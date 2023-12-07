from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import time

SLEEP_TIME = 0.5

class Sensor(ABC):
    def __init__(self, uuid):
        self.uuid = uuid
        self.state = 0

    @abstractmethod
    def get_sensor_state(self):
        pass

    def track_state_change(self):
        while True:
            if self.get_sensor_state() != self.state:
                self.state =  self.get_sensor_state()
                print(f'change in state to f{self.state}')

class IRMovementSensor(Sensor):
    def __init__(self, uuid, PIN):
        super().__init__(uuid)
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.IN)
    
    def get_sensor_state(self):
        return GPIO.input(self.PIN)

sensor = IRMovementSensor(13, 18)
sensor.track_state_change()