from enum import Enum


class SensorStatus(Enum):
    ERROR = -1
    TAKEN = 0
    AVAILABLE = 1


class Sensor:
    def __init__(self):
        print("Hello, I'm a sensor!")

