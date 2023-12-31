class Alarm:
    def __init__(self, controller, socket_server):
        self.controller = controller
        self.socket_server = socket_server

    def alarm(self, position):
        print(f'Alarm in the {position}')
        self.take_images(position)

    def take_images(self, position):
        available_cameras = [c for c in self.controller.reactors.values(
        ) if c['position'] == position and c['type'] == 'Camera']
        for camera in available_cameras:
            data = {'uuid': camera["uuid"], 'message': self.controller.cfg.get(
                'take_images_message'), 'num_images': self.controller.cfg.get('alarm_num_images'),
                'image_freq': self.controller.cfg.get('alarm_image_freq')}
            self.socket_server.send_data_to(data, camera['address'])
