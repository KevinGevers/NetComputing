#!/usr/bin/env python
import pika
from sensor import Sensor, SensorStatus



import json


class ParkingLot:
    status = {}
    sensors = []
    uid = -1
    queue = None
    channel = None

    reserved = set()

    def __init__(self, uid, manager_address):
        self.uid = uid
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters(manager_address))
        self.channel = queue_connection.channel()

    def sensor_update(self, sensor_status, sensor_id):
        print('Sensor update')
        if sensor_status == SensorStatus.AVAILABLE:
            self.reserved.add(sensor_id)
        else:
            self.reserved.remove(sensor_id)

        self.status['reserved'] = len(self.reserved)
        self.status['total'] = len(self.sensors)
        self.queue_update()

    def queue_update(self):
        self.channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(self.status))

        print(" [x] Sent Status")



lot = ParkingLot(1, 'localhost')
lot.sensor_update(SensorStatus.AVAILABLE, 1)