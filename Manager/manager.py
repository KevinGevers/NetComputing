import pika
import json
import time
import datetime
from threading import Lock, Event, _start_new_thread

POOL_TIME = 10 #Seconds
RESERVATION_DURATION = 60 * 2

class Manager:
    data_lock = Lock()
    thread_event = Event()
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
        _start_new_thread(self.listen_queue, ())
        _start_new_thread(self.reservation_cleaner, ())

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
        with self.data_lock:
            available = - self.reserved
            for key, value in self.parking_lots.items():
                available += value

            return available


    def make_reservation(self, client_id):
        with self.data_lock:
            now = datetime.datetime.now()
            expiration = now + datetime.timedelta(seconds=RESERVATION_DURATION)

            self.reservations[client_id] = expiration

            r = {
                'client_id': client_id,
                'start_time': now,
                'end_time': expiration
                }

            self.reservations[client_id] = r

            return r

    def delete_reservation(self, client_id):
        print('Delete:' + client_id)
        with self.data_lock:
            r = self.reservations.pop(client_id, None)
            print(r)

            return {
                'result' : not (r == None),
                'reservation' : r
                }

    def get_reservation(self, client_id):
        with self.data_lock:
            return self.reservations[client_id]

    def reservation_cleaner(self):
        while(not self.thread_event.wait(POOL_TIME)):
            with self.data_lock:
                keys = []
                for key, item in self.reservations.items():
                    print(key + ': ' + str(datetime.datetime.now()) + '  ' + str(item['end_time']))
                    if datetime.datetime.now() >= item['end_time']:
                        keys.append(key)
            for key in keys:
                print('Client: ' + key + ' reservation expired')
                print(self.delete_reservation(key))
            print('Cleanup finished')