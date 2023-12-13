import json

DEFAULT_CONFIG = {
    "server_ip": "192.168.178.38",
    "server_port": 50001,
    "device_data_message": "device data",
    "take_image_message": "take image",
    "periodical_device_data_push_time": 10,
    "sensor_sleep_time": 0.5,
    "alarm_num_images": 5,
}


class Config:
    def __init__(self):
        self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = DEFAULT_CONFIG

    def save_config(self):
        with open('config.json', 'w') as file:
            json.dump(self.config, file, indent=4)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
