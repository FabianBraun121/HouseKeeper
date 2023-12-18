import subprocess

def create_container(component, line, *args):
    # Generate Dockerfile content
    dockerfile_content = f'''
FROM your_base_image
CMD ["python", "{component.lower()}.py", {", ".join(args)}"]
'''

    # Write Dockerfile to disk
    dockerfile_path = f"{component.lower()}_Dockerfile{line}"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    # Build and run the Docker container
    subprocess.run(["docker", "build", "-t", f"{component.lower()}-image{line}", "-f", dockerfile_path, "."])
    subprocess.run(["docker", "run", "-d", f"--name={component.lower()}-container", f"{component.lower()}-image{line}"])

def main():
    with open("components.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        components = line.strip().split()
        component_type = components[0]
        create_container(component_type, i, *components[1:])

if __name__ == "__main__":
    main()