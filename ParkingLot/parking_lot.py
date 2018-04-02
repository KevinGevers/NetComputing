#!/usr/bin/env python
import pika
import json
from socket import *
import _thread

from ParkingLot.sensor import SensorStatus

BUFFER_SIZE = 128  # Small buffer for fast response

class ParkingLot:
    def __init__(self, uid, port):
        self.sensors = set()
        self.taken = set()
        self.uid = 'p-lot' + str(uid)
        self.port = port
        self.channel = None
        print('Started parking lot on port: ' + str(port))

    def set_manager(self, manager_address):
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters(manager_address))
        self.channel = queue_connection.channel()

    def handler(self, clientsock, addr):
        print('Received connection on port: ' + str(self.port))
        raw_data = clientsock.recv(BUFFER_SIZE)
        clientsock.close()

        data = json.loads( raw_data.decode('utf-8') )

        sensor_id = data['id']
        status = SensorStatus(data['status'])
        self.sensor_update(sensor_id, status)

    def start_server(self):
        address = ('localhost', self.port)
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serversock.bind(address)
        self.serversock.listen()
        while True:
            print('Waiting for connection...')
            clientsock, address = self.serversock.accept()
            _thread.start_new_thread(self.handler, (clientsock, address))

    def sensor_update(self, sensor_id, sensor_status):
        print('Sensor update')
        self.sensors.add(sensor_id)

        if sensor_status == SensorStatus.TAKEN:
            self.taken.add(sensor_id)
        else:
            self.taken.discard(sensor_id)

        status = {
            'id' : self.uid,
            'total' : len(self.sensors),
            'taken' : len(self.taken)
        }
        status['available'] = status['total'] - status['taken']

        self.queue_update(status)

    def queue_update(self, status):
        if not self.channel:
            print('Error: Parking lot id="{0}" has no Manager!'.format(self.uid))
            return

        self.channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(status))
        print(" [x] Sent Status")
        print(status)



