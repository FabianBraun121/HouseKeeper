from config import Config
from abc import ABC, abstractmethod, abstractproperty
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import uuid
import threading
import json
import socket
import logging

logging.disable(logging.CRITICAL)
GPIO.setmode(GPIO.BCM)


class Device(ABC):
    def __init__(self, config, position: str = None):
        self.cfg = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.cfg.get('server_ip'),
                               self.cfg.get('server_port'))
        self.device_data = {'type': self.type, 'uuid': str(uuid.uuid4()),
                            'position': position, 'message': self.cfg.get('device_data_message')}
        self.periodical_device_data_push()
        threading.Thread(target=self.listen_for_incoming_data).start()

    @abstractproperty
    def type(self):
        pass

    @abstractmethod
    def process_incoming_data(self, message):
        pass

    def listen_for_incoming_data(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            try:
                data = json.loads(data.decode('utf-8'))
                self.process_incoming_data(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")

    def periodical_device_data_push(self):
        self.socket.sendto(json.dumps(self.device_data).encode(
            'utf-8'), self.server_address)
        threading.Timer(self.cfg.get('periodical_device_data_push_time'),
                        self.periodical_device_data_push).start()


class Sensor(Device):
    def __init__(self, config, position):
        super().__init__(config, position)
        self.device_data['state'] = 0
        threading.Thread(target=self.track_state_change).start()

    @property
    def type(self):
        return 'Sensor'

    @abstractmethod
    def get_sensor_state(self):
        pass

    @abstractproperty
    def sensor_type(self):
        pass

    def track_state_change(self):
        if self.get_sensor_state() != self.device_data.get('state'):
            self.device_data['state'] = self.get_sensor_state()
            self.send_device_data_to_server()
        threading.Timer(self.cfg.get('sensor_sleep_time'),
                        self.track_state_change).start()

    def process_incoming_data(self, data):
        if self.uuid == data['uuid']:
            if data['message'] == self.cfg.get('device_data_message'):
                self.send_device_data_to_server()

    def send_device_data_to_server(self):
        json_data = json.dumps(self.device_data)
        self.socket.sendto(json_data.encode('utf-8'), self.server_address)


class IRMovementSensor(Sensor):
    def __init__(self, config, position, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        super().__init__(config, position)

    def get_sensor_state(self):
        return GPIO.input(self.pin)

    @property
    def sensor_type(self):
        sensor_type = "IR Movement Sensor"
        self.device_data['sensor_type'] = sensor_type
        return sensor_type


class Camera(Device):
    def __init__(self, config, position):
        super().__init__(config, position)
        self.image_fname = "img.jpg"
        self.picam2 = Picamera2()

    @property
    def gate(self):
        return self.cfg.get('reactor_gate')

    @property
    def type(self):
        return 'Camera'

    def process_incoming_data(self, data):
        if data.get('message', 0) == self.cfg.get('take_image_message'):
            print('image has been taken')
            image = self.take_image()
            self.upload_image_to_google_drive(image)

    def upload_image_to_google_drive(self, image):
        pass

    def take_image(self):
        self.picam2.start_and_capture_file(
            self.image_fname, delay=0, show_preview=False)
        with open(self.image_fname, 'rb') as file:
            image = file.read()
        return image


config = Config()
sensor = IRMovementSensor(config, 'Living room', 18)
camera = Camera(config, 'Living room')
