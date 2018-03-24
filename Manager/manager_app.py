import flask
import datetime

app = flask.Flask(__name__)

parking_spaces = {
    'total' : 20,
    'available' : 3,
    'reserved' : 1,
    'reserve_time' : 15*60
}

reservations = {}

@app.route('/parkingspaces', methods=['GET'])
def get_parkingspaces():
    if len(parking_spaces) == 0:
        flask.abort(404)
    return flask.jsonify(parking_spaces)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    if len(reservations) == 0:
        flask.abort(404)
    return flask.jsonify({'reservations': reservations})

@app.route('/reservations/<string:client_id>', methods=['GET'])
def get_reservation(client_id):
    if not client_id in reservations:
        flask.abort(404)
    return flask.jsonify({'reservation': reservations[client_id]})

@app.route('/reservations', methods=['POST'])
def create_reservation():
    if not flask.request.json or not 'id' in flask.request.json:
        flask.abort(400)

    client_id = flask.request.json['id']
    if client_id in reservations:
        flask.abort(404)
    if parking_spaces['available'] - parking_spaces['reserved'] <= 0:
        return flask.jsonify({}), 204

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=parking_spaces['reserve_time'])
    reservation = {
        'client_id': client_id,
        'start_time': start_time,
        'end_time' : end_time
    }

    parking_spaces['reserved'] += 1

    reservations[client_id] = reservation
    return flask.jsonify({'reservation': reservation}), 201

@app.route('/reservations/<string:client_id>', methods=['DELETE'])
def delete_reservation(client_id):
    reservation = reservations.pop(client_id, None)
    if reservation is None:
        flask.abort(404)
    parking_spaces['reserved'] -= 1
    return flask.jsonify({
                            'result': True,
                            'reservation' : reservation
                         })

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

if __name__ == '__main__':
    app.run(debug=True)
