from enum import Enum
import socket
import time
import random
import json


class SensorStatus(Enum):
    ERROR = -1
    TAKEN = 0
    AVAILABLE = 1


class Sensor:
    uid = ''
    host = None
    host_port = -1
    status = SensorStatus.AVAILABLE

    def __init__(self, host, host_port):
        self.uid = 'sensor-' + str(random.randint(0, 9999))
        self.host = host
        self.host_port = host_port



    def update(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.host_port))

        if server:
            data = {
                'id' : self.uid,
                'status' : self.status.value
            }

            str = json.dumps(data)
            print(str)
            server.send(str.encode())


if __name__ == "__main__":
    for i in range(0, 30):
        time.sleep(.1)
        sensor = Sensor('127.0.0.1', 6606)
        sensor.status = SensorStatus(random.randint(0, 1))
        sensor.update()


