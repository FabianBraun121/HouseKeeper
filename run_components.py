import re
import os
import yaml

def initialize_docker_compose():
    # Initialize an empty Docker Compose dictionary
    docker_compose = {'version': '3', 'services': {}}
    return docker_compose

def add_service(docker_compose, component, line, *args):
    # Add a new service to the Docker Compose dictionary
    service_name = f'{line}_{component}'
    docker_compose['services'][service_name] = {'image': 'fabianbraun121/housekeeper:latest'}

    # Add optional parameters if provided
    command = f'python3 base_container/run_{component.lower()}.py{" ".join(map(str, args))}'
    docker_compose['services'][service_name]['command'] = command
    volume = '/home/pi/HouseKeeper/secret_config.json:/app/HouseKeeper/secret_config.json'
    docker_compose['services'][service_name]['volumes'] = [volume]
    docker_compose['services'][service_name]['network_mode'] = 'host'
    docker_compose['services'][service_name]['privileged'] = True
    docker_compose['services'][service_name]['environment'] = ['UDEV=1']

def generate_docker_compose_file():
    docker_compose = initialize_docker_compose()

    with open("components.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        line = re.sub(r'"([^"]*)"', lambda x: x.group(0).replace(' ', '|'), line)
        line = re.sub(r"'([^']*)'", lambda x: x.group(0).replace(' ', '|'), line)
        components = line.strip().split()
        components = [arg.replace('|', ' ') for arg in components]
        component_type = components[0]

        add_service(docker_compose, component_type, i, *components[1:])
    
    with open("docker-compose.yml", "w") as file:
        yaml.dump(docker_compose, file)

def main():
    cleanup()
    generate_docker_compose_file()
    os.system("docker-compose up --build -d")

def cleanup():
    os.system("docker-compose down -v")

if __name__ == "__main__":
    main()
