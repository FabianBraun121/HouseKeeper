import threading
from config import Config
from communication_server import CommunicationServer
from alarm import Alarm


class Controller:
    def __init__(self, config):
        self.cfg = config
        self.sensors = {}
        self.sensors_lock = threading.Lock()
        self.reactors = {}
        self.reactors_lock = threading.Lock()
        self.communication_server = CommunicationServer(self)
        self.alarm = Alarm(self)
        self.position_relation = None

    def start(self):
        self.alarm.start()
        self.communication_server.start()

    def stop(self):
        self.alarm.stop()
        self.communication_server.stop()

    def process_sensor_state(self, sensor_data):
        with self.sensors_lock:
            uuid = sensor_data['uuid']
            current_state = self.sensors.get(uuid, {}).get('state', 0)

            if current_state != 1 and sensor_data['state'] == 1:
                threading.Thread(target=self.alarm.alarm(
                    sensor_data['position'])).start()

            self.sensors[uuid] = sensor_data

    def initialize_divice(self, device_data):
        if device_data['type'] == 'Sensor':
            if device_data['uuid'] not in self.sensors:
                with self.sensors_lock:
                    self.sensors[device_data['uuid']] = device_data
        else:
            if device_data['uuid'] not in self.reactors:
                with self.reactors_lock:
                    self.reactors[device_data['uuid']] = device_data


config = Config()
controller = Controller(config)
controller.start()
