from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, uuid):
        self.uuid = uuid

    @abstractmethod
    def get_sensor_state(self):
        pass