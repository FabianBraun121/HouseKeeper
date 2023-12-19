import subprocess

def create_container(component, line, *args):
    # Generate Dockerfile content
    dockerfile_content = f'''
FROM fabianbraun121/housekeeper:latest
CMD ["python", "base_container/run_{component.lower()}.py", {", ".join(args)}"]
'''

    # Write Dockerfile to disk
    dockerfile_path = f"{component.lower()}_Dockerfile{line}"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    # Build and run the Docker container with specific flags
    subprocess.run([
        "docker", "build", "-t", f"{component.lower()}-image{line}", "-f", dockerfile_path, "."
    ])
    subprocess.run([
        "docker", "run", "-it", "--rm", "--network", "host",
        "-v", "$HOME/Documents/HouseKeeper/base_container/secret_config.json:/app/Documents/HouseKeeper/base_container/secret_config.json",
        "--privileged", "--env", "UDEV=1",
        f"--name={component.lower()}-container", f"{component.lower()}-image{line}"
    ])

def main():
    with open("components.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        components = line.strip().split()
        component_type = components[0]
        create_container(component_type, i, *components[1:])

if __name__ == "__main__":
    main()