import socket
import threading
import json
from device_initializer import DeviceInitializer
from sensor_listener import SensorListener
from alarm import Alarm


class Controller:
    def __init__(self, config):
        self.cfg = config
        self.sensors = dict
        self.reactors = dict
        self.alarm = Alarm(self)
        self.position_relation = None

    def start(self):
        DeviceInitializer(self).start()
        SensorListener(self).start()

    def update_sensor_state(self, data):
        if self.sensors[data['uuid']]['state'] != 1 and data['state'] == 1:
            self.alarm.alarmize(data['position'])
        self.sensors[data['uuid']] = data

    def alarm(self, data: dict):
        print(f'Alarm, in the {data["position"]}')
        for device in self.device_address.values():
            if device['type'] == 'Camera' and device['position'] == data['position']:
                self.camera_socket.sendto(
                    "Take Images".encode('utf-8'), device['address'])


from config import Config
config = Config()
controller = Controller()