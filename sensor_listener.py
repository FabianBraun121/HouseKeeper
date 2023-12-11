import socket
import threading
import json
from controller import Controller

class SensorListener:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.cfg = self.controller.cfg
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.cfg.get('central_ip'), self.cfg.get('sensor_gate'))
        self.socket.bind(self.sensor_address)

    def start(self):
        threading.Thread(target=self.process_message).start()

    def process_message(self):
        while True:
            data, address = self.sensor_socket.recvfrom(1024)
            try:
                data = json.loads(data.decode('utf-8'))
                data['address'] = address
                self.controller.update_sensor_state(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")