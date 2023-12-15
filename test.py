from remote_server_client import RemoteServerClient
from config import Config


config = Config()
remote_server_client = RemoteServerClient(config)

#remote_server_client.upload_file("google_logo.jpg", "logo_test11.jpg")
print(remote_server_client.get_file_info_list())