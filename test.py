from config import Config
from remote_server_client import RemoteServerClient

config = Config()
remote_server_client = RemoteServerClient(config)
key = remote_server_client.get_file_info_list()[-1][0]
remote_server_client.download_file(key, 'test1.jpg')