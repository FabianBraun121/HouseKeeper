import time


class Alarm:
    def __init__(self, controller, communication_server):
        self.controller = controller
        self.communication_server = communication_server

    def alarm(self, position):
        print(f'Alarm in the {position}')
        self.take_images(position)

    def take_images(self, position):
        if self.controller.position_relation is not None:
            pass  # needs to be implemented first
        else:
            available_cameras = [c for c in self.controller.reactors.values(
            ) if c['position'] == position and c['type'] == 'Camera']
        for _ in range(self.controller.cfg.get('alarm_num_images')):
            for camera in available_cameras:
                data = {'uuid': camera["uuid"], 'message': self.controller.cfg.get(
                    'take_image_message')}
                self.communication_server.send_data_to(data, camera['address'])
            time.sleep(1)
