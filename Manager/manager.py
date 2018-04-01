import pika
import json
import time
import _thread

#TODO: create data lock.

POOL_TIME = 60 #Seconds
RESERVATION_DURATION = 60 * 2

class Manager:
    location = {
        'longitude': 0.0,
        'latitude': 0.0
        }
    running = True
    parking_lots = {}
    reservations = {}

    def __init__(self):
        queue_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = queue_connection.channel()
        self.channel.queue_declare(queue='hello')
        self.channel.basic_consume(self.handler, queue='hello', no_ack=True)


    def handler(self, ch, method, properties, body):
        msg = body.decode('utf-8')
        data = json.loads(msg)

        print(' [x] Received parking status.')

        parking_id = data['id']
        data['available'] = data['total'] - data['reserved']

        self.parking_lots[parking_id] = data

        print(self.get_status())


    def start(self):
        _thread.start_new_thread(self.listen_queue, ())
        _thread.start_new_thread(self.reservation_cleaner, ())

    def listen_queue(self):
        print(' [*] Waiting for messages.')
        self.channel.start_consuming()


    def set_location(self, lon, lat):
        self.location['longitude'] = lon
        self.location['latitude'] = lat


    def get_status(self):
        status = {
                'total' : 0,
                'reserved' : 0,
                'available' : 0
                }


        for (p_id, data) in self.parking_lots.items():
            status['total'] += data['total']
            status['reserved'] += data['reserved']
            status['available'] += data['available']
        return status


    def get_available(self):
        available = - self.reserved
        for key, value in self.parking_lots.items():
            available += value

        return available


    def make_reservation(self, client_id):
        now = int(time.time())
        expiration = now + RESERVATION_DURATION

        self.reservations[client_id] = expiration

        r = {
            'client_id': client_id,
            'start_time': now,
            'end_time': expiration
            }

        self.reservations[client_id] = r

        return r

    def delete_reservation(self, client_id):
        reservation = self.reservations.pop(client_id, None)

        return {
            'result' : not (reservation == None),
            'reservation' : reservation
            }

    def get_reservation(self, client_id):
        return self.reservations[client_id]

    def reservation_cleaner(self):
        while self.running:
            time.sleep(5)
        print('end')

'''
manager = Manager()
manager.start()

while(True):
    pass
'''