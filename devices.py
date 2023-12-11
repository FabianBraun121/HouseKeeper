from abc import ABC, abstractmethod, abstractproperty
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import uuid
import threading
import json
import socket
GPIO.setmode(GPIO.BCM)


class Device(ABC):
    def __init__(self, config, position: str = None):
        self.cfg = config
        self.uuid = str(uuid.uuid4())
        self.position = position
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        initial_data = {'type': self.type,
                        'uuid': self.uuid, 'position': self.position}
        self.socket.sendto(json.dumps(initial_data).encode(
            'utf-8'), (self.cfg.get('central_ip'), self.cfg.get('initialization_gate')))
        self.socket.bind(self.cfg.get('central_ip'), self.gate)
        threading.Thread(target=self.listen_for_message).start()

    @abstractproperty
    def type(self):
        pass

    @abstractproperty
    def gate(self):
        pass

    @abstractmethod
    def process_message(self, message):
        pass

    def listen_for_message(self):
        while True:
            data, _ = self.socket.recvfrom(1024)
            try:
                message = json.loads(data.decode('utf-8'))
                self.process_message(message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")


class Sensor(Device):
    def __init__(self, config, position):
        super().__init__(config, position)
        self.state = 0
        threading.Thread(target=self.track_state_change).start()

    @property
    def type(self):
        return 'Sensor'

    @property
    def gate(self):
        return self.cfg.get('sensor_gate')

    @abstractmethod
    def get_sensor_state(self):
        pass

    @abstractproperty
    def sensor_type(self):
        pass

    def track_state_change(self):
        if self.get_sensor_state() != self.state:
            self.state = self.get_sensor_state()
            self.send_state_to_server()
        threading.Timer(self.cfg.get('sensor_sleep_time'),
                        self.track_state_change).start()

    def process_message(self, message):
        if self.uuid == message['uuid']:
            if message['message'] == 'get state':
                self.send_state_to_server()

    def send_state_to_server(self):
        data_to_send = {'type': self.type, 'uuid': self.uuid, 'state': self.state,
                        'position': self.position, 'sensor type': self.sensor_type}
        json_data = json.dumps(data_to_send)
        self.server_socket.send(json_data.encode('utf-8'))


class IRMovementSensor(Sensor):
    def __init__(self, config, position, pin):
        super().__init__(config, position)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def get_sensor_state(self):
        return GPIO.input(self.pin)

    @property
    def sensor_type(self):
        return "IR Movement Sensor"


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

    def process_message(self, message):
        if self.uuid == message['uuid']:
            if message['message'] == 'take image':
                self.send_image_to_server()

    def send_image_to_server(self):
        self.take_image()
        with open(self.image_fname, 'rb') as file:
            image_data = file.read()
        data_to_send = {'type': self.type, 'uuid': self.uuid,
                        'position': self.position, 'image': image_data}
        self.socket.send(json.dumps(data_to_send).encode('utf-8'))

    def take_image(self):
        self.picam2.start_and_capture_file(
            self.image_fname, delay=0, show_preview=False)


from config import Config
config = Config()
sensor = IRMovementSensor(config, 'Living room', 18)
camera = Camera(config, 'Living room')
