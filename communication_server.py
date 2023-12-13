import socket
import threading
import json


class CommunicationServer:
    def __init__(self, controller):
        self.controller = controller
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.controller.cfg.get('server_ip'),
                          self.controller.cfg.get('server_port')))
        self.is_listening = False

    def start(self):
        self.is_listening = True
        threading.Thread(target=self.process_incoming_messages).start()

    def stop(self):
        self.is_listening = False

    def process_incoming_messages(self):
        while self.is_listening:
            data, address = self.socket.recvfrom(1024)
            try:
                data = json.loads(data.decode('utf-8'))
                data['address'] = address
                message_type = data['message']
                if message_type == self.controller.cfg.get('device_data'):
                    self.controller.process_device_data(data)
                else:
                    raise ValueError(f"Unknown message type {message_type}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")

    def send_data_to(self, data, address):
        encoded_data = json.dumps(data).encode('utf-8')
        self.socket.sendto(encoded_data, address)
