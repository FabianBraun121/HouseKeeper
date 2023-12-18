from config import Config
from controller import Controller

def main():
    config = Config()
    controller = Controller(config)
    controller.start()

if __name__ == '__main__':
    main()