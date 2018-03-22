from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

parking_spaces = {
    'total' : 20,
    'available' : 5,
    'reserved' : 1
}

reservations = [
    {
        'client_id' : 'test',
        'start_time' : '2012-04-23T18:25:43.511Z'
    }
]

@app.route('/parkingspaces', methods=['GET'])
def get_parkingspaces():
    if len(parking_spaces) == 0:
        abort(404)
    return jsonify(parking_spaces)

@app.route('/reservations', methods=['GET'])
def get_reservation():
    if len(reservations) == 0:
        abort(404)
    return jsonify({'reservations': reservations})

def get_reservation(client_id):
    reservation = [reservation for reservation in reservations if reservation['client_id'] == client_id]
    if len(reservation) == 0:
        abort(404)
    return jsonify({'reservation': reservation[0]})

def create_reservation():
    return 'Not implemented yet'

def delete_reservation():
    return 'Not implemented yet'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
