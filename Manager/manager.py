import pika
import json


class Location:
    longitude = 0
    latitude = 0


class Manager:
    parking_lots = {}
    reserved = 0
    channel = None

    def handler(self, ch, method, properties, body):
        msg = body.decode('utf-8')
        data = json.loads(msg)

        print(' [x] Received parking status.')
        print(data)

        parking_id = data['id']
        total = data['total']
        reserved = data['reserved']

        self.parking_lots[parking_id] = total - reserved

    def __init__(self):
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = queue_connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.basic_consume(self.handler, queue='hello', no_ack=True)

    def listen_queue(self):
        print(' [*] Waiting for messages.')
        self.channel.start_consuming()

    def spots_available(self):
        available = - self.reserved
        for key, value in self.parking_lots.items():
            available += value

        return available


manager = Manager()
manager.listen_queue()
