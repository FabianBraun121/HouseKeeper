import re
import os
from jinja2 import Template

def generate_docker_compose(lines):
    template_content = '''\
    version: '3'
    services:
    {% for i, line in enumerate(lines) %}
      {{ component_type }}_{{ i }}:
        image: fabianbraun121/housekeeper:latest
        command: ["python3", "base_container/run_{{ component_type.lower() }}.py", {{ components[1:] }}]
        network_mode: host
        privileged: true
        volumes:
          - /home/pi/Documents/HouseKeeper/secret_config.json:/app/Documents/HouseKeeper/secret_config.json
        environment:
          - UDEV=1
    {% endfor %}
    '''

    template = Template(template_content)
    rendered_template = template.render(lines=lines)
    with open("docker-compose.yml", "w") as compose_file:
        compose_file.write(rendered_template)

def main():
    with open("components.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        line = re.sub(r'"([^"]*)"', lambda x: x.group(0).replace(' ', '|'), line)
        line = re.sub(r"'([^']*)'", lambda x: x.group(0).replace(' ', '|'), line)
        components = line.strip().split()
        components = [arg.replace('|', ' ') for arg in components]
        component_type = components[0]

    generate_docker_compose(lines)

    # Build and run containers using Docker Compose
    os.system("docker-compose up --build -d")

def cleanup():
    os.system("docker-compose down -v")

if __name__ == "__main__":
    cleanup()
    main()
