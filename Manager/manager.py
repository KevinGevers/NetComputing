import pika
import json
import datetime
from threading import Lock, Event, _start_new_thread

POOL_TIME = 10 #Seconds
RESERVATION_DURATION = 60 * 2

'''
This Class is the ParkingLot Manager
ParkingLots at the Manager's location update the Manager with their availability status.
The manager joins all the ParkingLots to obtain the total availability at the location.

The manager is also in charge of making reservations through a REST interface. See: 'manager_app.py'
Reservations are removed when expired.

The manager also holds all the data inside the class as there is currently no external database.
'''
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
        data['available'] = data['total'] - data['taken']

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
                'reserved' : len(self.reservations),
                'available' : -len(self.reservations)
                }

        for (p_id, data) in self.parking_lots.items():
            status['total'] += data['total']
            status['available'] += data['available']
        return status


    def get_available(self):
        with self.data_lock:
            return self.get_status()['available']


    def make_reservation(self, client_id):
        # Return null of no spaces left
        if self.get_available() <= 0:
            return None
        # If already has a reservation return it.
        if client_id in self.reservations:
            return self.get_reservation(client_id)
        # Otherwise, make reservation
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


    # This method deletes expired reservations
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