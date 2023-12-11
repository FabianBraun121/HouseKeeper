import socket
import threading
import json


class DeviceInitializer:
    def __init__(self, controller):
        self.controller = controller
        self.cfg = self.controller.cfg
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.cfg.get('central_ip'),
                        self.cfg.get('initialization_gate'))
        self.socket.bind(self.address)

    def start(self):
        threading.Thread(target=self.process_initializations).start()

    def process_initializations(self):
        while True:
            data, address = self.socket.recvfrom(1024)
            try:
                data = json.loads(data.decode('utf-8'))
                data['address'] = address
                if data['type'] == 'Sensor':
                    if data['uuid'] not in self.controller.sensors:
                        self.controller.sensors[data['uuid']] = data
                else:
                    if data['uuid'] not in self.controller.reactors:
                        self.controller.reactors[data['uuid']] = data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
