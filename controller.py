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
        self.alarm = Alarm(self, self.communication_server)
        self.position_relation = None

    def start(self):
        print('starting the alarm system')
        self.communication_server.start()

    def stop(self):
        print('stoping the alarm system')
        self.communication_server.stop()

    def process_device_data(self, device_data):
        if any(device_data['uuid'] not in d for d in (self.sensors, self.reactors)):
            self.initialize_divice(device_data)
        if device_data['uuid'] in self.sensors:
            with self.sensors_lock:
                uuid = device_data['uuid']
                current_state = self.sensors.get(uuid).get('state', 0)

                cast_alarm = current_state != 1 and device_data['state'] == 1
                self.sensors[uuid] = device_data

            if cast_alarm:
                threading.Thread(target=self.alarm.alarm(
                    device_data['position'])).start()

    def initialize_divice(self, device_data):
        if device_data['type'] == 'Sensor':
            with self.sensors_lock:
                device_data['state'] = 0
                self.sensors[device_data['uuid']] = device_data
        else:
            with self.reactors_lock:
                self.reactors[device_data['uuid']] = device_data


config = Config()
controller = Controller(config)
controller.start()
