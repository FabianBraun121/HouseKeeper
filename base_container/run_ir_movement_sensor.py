from config import Config
from devices import IRMovementSensor
import sys

def main(position, pin):
    config = Config()
    IRMovementSensor(config, position, pin)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)