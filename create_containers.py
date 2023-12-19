import subprocess
import re
import os


def create_container(component, line, *args):
    # Generate Dockerfile content
    dockerfile_content = f'''
FROM fabianbraun121/housekeeper:latest
CMD ["python3", "base_container/run_{component.lower()}.py", {", ".join(map(repr, args))}]
'''

    # Write Dockerfile to disk
    dockerfile_path = f"dockerfiles/{component.lower()}_Dockerfile{line}"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    # Build and run the Docker container with specific flags
    subprocess.run([
        "docker", "build", "-t", f"{component.lower()}-image{line}", "-f", dockerfile_path, "./dockerfiles"
    ])
    subprocess.run([
        "docker", "run", "--rm", "--network", "host", "--privileged", 
        "-v", "/home/pi/Documents/HouseKeeper/secret_config.json:/app/Documents/HouseKeeper/secret_config.json",
        "-e", "UDEV=1",
        f"--name={component.lower()}-container{line}", f"{component.lower()}-image{line}"
    ])


def delete_old_dockerfiles(path):
    files = os.listdir(path)
    for file in files:
        os.remove(os.path.join(path,file))

def main():
    delete_old_dockerfiles("dockerfiles")

    with open("components.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # Replace spaces within single or double quotes with a placeholder
        line = re.sub(r'"([^"]*)"' , lambda x: x.group(0).replace(' ', '|'), line)
        line = re.sub(r"'([^']*)'", lambda x: x.group(0).replace(' ', '|'), line)
        components = line.strip().split()

        # Replace the placeholders back with spaces in each argument
        components = [arg.replace('|', ' ') for arg in components]

        component_type = components[0]
        create_container(component_type, i, *components[1:])

if __name__ == "__main__":
    main()