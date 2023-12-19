from config import Config
from devices import Camera
from remote_server_client import RemoteServerClient
import sys

def main(position):
    config = Config()
    remote_server_client = RemoteServerClient(config)
    Camera(config, str(position), remote_server_client)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)