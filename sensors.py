from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import uuid
import threading
GPIO.setmode(GPIO.BCM)

SLEEP_TIME = 0.5

class Sensor(ABC):
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0

    @abstractmethod
    def get_sensor_state(self):
        pass

    def track_state_change(self):
        if self.get_sensor_state() != self.state:
            self.state =  self.get_sensor_state()
            print(f'change in state to f{self.state}')
        threading.Timer(SLEEP_TIME, self.track_state_change).start()
        

class IRMovementSensor(Sensor):
    def __init__(self, PIN):
        super().__init__()
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.IN)
    
    def get_sensor_state(self):
        return GPIO.input(self.PIN)

sensor = IRMovementSensor(18)
sensor.track_state_change()