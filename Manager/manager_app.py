import flask
from Manager.manager import Manager

'''
MODIFICATIONS BY RAUL

* Get reservations from Manager class
* Moved reservation cleaner to the Manager class (REST service should only be used for data/state transfer)
* Removed make_public_reservation: Redundant since the client knows his client and can construct the URL without help (wastes time + bandwidth)
* Empty data now returns empty data and not 400.
* Minor modifications to error handlers
'''

app = flask.Flask(__name__)


@app.route('/parkingspaces', methods=['GET'])
def get_parkingspaces():
    return flask.jsonify( manager.get_status() )


@app.route('/reservations', methods=['GET'])
def get_reservations():
    return flask.jsonify(manager.reservations )


@app.route('/reservations/<string:client_id>', methods=['GET'])
def get_reservation(client_id):
    if client_id not in manager.reservations:
        flask.abort(400)

    return flask.jsonify( manager.get_reservation(client_id))


@app.route('/reservations', methods=['POST'])
def create_reservation():
    print('Reservation post ' + str(flask.request.json))

    if not flask.request.json or not 'id' in flask.request.json:
        flask.abort(400)

    client_id = flask.request.json['id']
    if client_id in manager.reservations:
        return flask.jsonify( manager.get_reservation(client_id) )

    return flask.jsonify( manager.make_reservation(client_id) )


@app.route('/reservations/<string:client_id>', methods=['DELETE'])
def delete_reservation(client_id):
    return flask.jsonify( manager.delete_reservation(client_id) )


@app.errorhandler(400)
def bad_request(error):
    return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(403)
def forbidden(error):
    return flask.make_response(flask.jsonify({'error': 'Forbidden'}), 403)

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

@app.errorhandler(501)
def not_implemented(error):
    return flask.make_response(flask.jsonify({'error': 'Not implemented'}), 501)


if __name__ == '__main__':
    manager = Manager()
    manager.start()
    app.run(debug=True, port=5000)
