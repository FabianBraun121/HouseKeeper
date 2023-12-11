from config import Config
from device_initializer import DeviceInitializer
from sensor_listener import SensorListener
from alarm import Alarm


class Controller:
    def __init__(self, config):
        self.cfg = config
        self.sensors = {}
        self.reactors = {}
        self.alarm = Alarm(self)
        self.position_relation = None

    def start(self):
        DeviceInitializer(self).start()
        SensorListener(self).start()

    def update_sensor_state(self, data):
        print(self.sensors[data['uuid']])
        if self.sensors[data['uuid']].get('state', 0) != 1 and data['state'] == 1:
            self.alarm.alarmize(data['position'])
        self.sensors[data['uuid']] = data


config = Config()
controller = Controller(config)
controller.start()
