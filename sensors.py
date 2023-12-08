from abc import ABC, abstractmethod, abstractproperty
import RPi.GPIO as GPIO
import uuid
import threading
import json
import socket
from constants import SENSOR_SLEEP_TIME, CENTRAL_IP, CENTRAL_GATE
GPIO.setmode(GPIO.BCM)


class Sensor(ABC):
    def __init__(self, position:str=None):
        self.uuid = str(uuid.uuid4())
        self.state = 0
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.position = position
        # send intial state to the server
        self.send_state_to_server()

    @abstractmethod
    def get_sensor_state(self):
        pass
    
    @abstractproperty
    def sensor_type(self):
        pass

    def track_state_change(self):
        if self.get_sensor_state() != self.state:
            self.state =  self.get_sensor_state()
            self.send_state_to_server()
        threading.Timer(SENSOR_SLEEP_TIME, self.track_state_change).start()
    
    def send_state_to_server(self):
        data_to_send = {'uuid': self.uuid, 'position': self.position, 'sensor type': self.sensor_type}
        json_data = json.dumps(data_to_send)
        self.server_socket.sendto(json_data.encode('utf-8'), (CENTRAL_IP,CENTRAL_GATE))
        

class IRMovementSensor(Sensor):
    def __init__(self, PIN, position:str=None):
        self.PIN = PIN
        super().__init__(position)
        GPIO.setup(self.PIN, GPIO.IN)
    
    def get_sensor_state(self):
        return GPIO.input(self.PIN)
    
    @property
    def sensor_type(self):
        return "IR Movement Sensor"

sensor = IRMovementSensor(18, position='Living room')
sensor.track_state_change()