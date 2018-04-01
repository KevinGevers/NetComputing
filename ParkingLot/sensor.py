from enum import Enum
import socket
import json


class SensorStatus(Enum):
    ERROR = -1
    TAKEN = 0
    AVAILABLE = 1


class Sensor:
    status = SensorStatus.AVAILABLE

    def __init__(self, uid, host, host_port):
        self.uid = 'sensor-' + str(uid)
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

    def trigger(self):
        if(self.status == SensorStatus.AVAILABLE):
            self.status = SensorStatus.TAKEN
        else:
            self.status = SensorStatus.AVAILABLE

        self.update()


