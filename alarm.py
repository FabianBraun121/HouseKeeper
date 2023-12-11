import socket
import threading
import time
import json
from controller import Controller


class Alarm:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.cfg = self.controller.cfg
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.cfg.get('central_ip'),
                        self.cfg.get('reactor_gate'))
        self.socket.bind(self.address)
        threading.Thread(target=self.process_incoming_data).start()

    def alarmize(self, position):
        print(f'Alarm in the {position}')
        threading.Thread(target=self.take_images, args=(position,)).start()

    def process_incoming_data(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            try:
                received_data = json.loads(data.decode('utf-8'))
                image_data = received_data.get('image')
                with open('received_img.jpg', 'wb') as file:
                    file.write(image_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")

    def take_images(self, position):
        if self.controller.position_relation is not None:
            pass  # needs to be implemented first
        else:
            available_cameras = [c for c in self.controller.reactors.items(
            ) if c['position'] == position and c['type'] == 'Camera']
        for _ in range(self.cfg.get('alarm_num_images')):
            for camera in available_cameras:
                message = {'uuid': camera["uuid"], 'action': 'take image'}
                self.socket.sendto(json.dumps(message).encode(
                    'utf-8'), camera['address'])
            time.sleep(1)
