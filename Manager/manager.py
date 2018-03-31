import pika
import json



class Manager():
    total = 0
    reserved = 0
    channel = None

    def handler(self, ch, method, properties, body):
        msg = body.decode('utf-8')
        data = json.loads(msg)

        print(' [x] Received parking status.')
        print(data)

        self.total = data['total']
        self.reserved = data['reserved']


    def __init__(self):
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = queue_connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.basic_consume(self.handler, queue='hello', no_ack=True)

    def listen_queue(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()



manager = Manager()
manager.listen_queue()
