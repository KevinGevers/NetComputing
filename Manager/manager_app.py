import flask
import datetime
import threading
import atexit

app = flask.Flask(__name__)
POOL_TIME = 60 #Seconds

parking_spaces = {
    'total' : 20,
    'available' : 3,
    'reserve_time' : 2*60
}

reservations = {}

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

#Makes an uri from the client_id
def make_public_reservation(reservation):
    new_reservation = {}
    for field in reservation:
        if field == 'client_id':
            new_reservation['uri'] = flask.url_for('get_reservation', client_id=reservation['client_id'], _external=True)
        else:
            new_reservation[field] = reservation[field]
    return new_reservation

@app.route('/parkingspaces', methods=['GET'])
def get_parkingspaces():
    if len(parking_spaces) == 0:
        flask.abort(404)
    r = parking_spaces
    with dataLock:
        r['reservations'] = len(reservations)
    return flask.jsonify(r)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    with dataLock:
        if len(reservations) == 0:
            flask.abort(404)
        reservations_uri = [make_public_reservation(reservation) for key, reservation in reservations.items()]
    return flask.jsonify({'reservations': reservations_uri})

@app.route('/reservations/<string:client_id>', methods=['GET'])
def get_reservation(client_id):
    with dataLock:
        if not client_id in reservations:
            flask.abort(404)
        reservation = reservations[client_id]
    return flask.jsonify({'reservation': reservation})

@app.route('/reservations', methods=['POST'])
def create_reservation():
    if not flask.request.json or not 'id' in flask.request.json:
        flask.abort(400)

    client_id = flask.request.json['id']
    if client_id in reservations:
        flask.abort(404)
    with dataLock:
        if parking_spaces['available'] - len(reservations) <= 0:
            return flask.jsonify({}), 204
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=parking_spaces['reserve_time'])
        reservation = {
            'client_id': client_id,
            'start_time': start_time,
            'end_time' : end_time
        }

        reservations[client_id] = reservation
    return flask.jsonify({'reservation': make_public_reservation(reservation)}), 201

@app.route('/reservations/<string:client_id>', methods=['DELETE'])
def delete_reservation_wrapper(client_id):
    reservation = None
    with dataLock:
        reservation = delete_reservation(client_id)
    if reservation is None:
        flask.abort(404)

    return flask.jsonify({
                            'result': True,
                            'reservation' : reservation
                         })

def delete_reservation(client_id):
    reservation = reservations.pop(client_id, None)
    return reservation

@app.errorhandler(400)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(403)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), 403)

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

@app.errorhandler(501)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not implemented'}), 501)

#Reservation cleanup thread
class reservations_cleanup(threading.Thread):
    def __init__(self,reservations,lock):
        threading.Thread.__init__(self)
        self.reservations = reservations
        self.lock = lock
        self.stop = threading.Event()

    def run(self):
        print('Startin cleanup thread')
        while(not self.stop.wait(POOL_TIME)):
            with self.lock:
                keys = []
                for key, item in self.reservations.items():
                    print(key + ': ' + str(datetime.datetime.now()) + '  ' + str(item['end_time']))
                    if datetime.datetime.now() >= item['end_time']:
                        keys.append(key)
                for key in keys:
                    print('Client: ' + key + ' reservation expired')
                    delete_reservation(key)
            print('Cleanup finished')

cleaner = reservations_cleanup(reservations,dataLock)

def exit_cleanup():
    global cleaner
    cleaner.stop.set()
    cleaner.join()
    print('Exiting manager webservice')

if __name__ == '__main__':
    cleaner.start()
    atexit.register(exit_cleanup)
    app.run(debug=True)
