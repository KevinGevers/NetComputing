#!/usr/bin/env python
import pika
import json
from socket import *
import _thread

from ParkingLot.sensor import SensorStatus

BUFFER_SIZE = 128  # Small buffer for fast response
HOST = '127.0.0.1'
PORT = 6606


class ParkingLot:
    sensors = set()
    reserved = set()
    uid = -1
    channel = None


    def __init__(self, uid, manager_address):
        self.uid = uid
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters(manager_address))
        self.channel = queue_connection.channel()

    def handler(self, clientsock, addr):
        raw_data = clientsock.recv(BUFFER_SIZE)
        clientsock.close()

        data = json.loads( raw_data.decode('utf-8') )

        sensor_id = data['id']
        status = SensorStatus(data['status'])
        self.sensor_update(sensor_id, status)

    def start_server(self):
        address = (HOST, PORT)
        serversock = socket(AF_INET, SOCK_STREAM)
        serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serversock.bind(address)
        serversock.listen()
        while True:
            print('Waiting for connection...')
            clientsock, address = serversock.accept()
            _thread.start_new_thread(self.handler, (clientsock, address))

    def sensor_update(self, sensor_id, sensor_status):
        print('Sensor update')
        self.sensors.add(sensor_id)

        if sensor_status == SensorStatus.AVAILABLE:
            self.reserved.add(sensor_id)
        else:
            self.reserved.discard(sensor_id)

        status = {
            'id' : self.uid,
            'total' : len(self.sensors),
            'reserved' : len(self.reserved)
        }

        status['reserved'] = len(self.reserved)
        status['total'] = len(self.sensors)
        self.queue_update(status)


    def queue_update(self, status):
        self.channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(status))
        print(" [x] Sent Status")


lot = ParkingLot(1, 'localhost')
lot.start_server()