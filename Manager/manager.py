import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

class Manager():

    channel = None

    def __init__(self):
        print("Hi, I'm a manager")
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = queue_connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.basic_consume(callback, queue='hello', no_ack=True)

    def listen_queue(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()



manager = Manager()
manager.listen_queue()
