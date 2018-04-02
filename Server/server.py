#!flask/bin/python
from flask import Flask, jsonify
#from flask import make_response
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the server'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

managers = [
    {
        'id' : 1,
        'manager_url' : 'http://127.0.0.1:5001',
        'manager_location_latitude' : 53.2405038,
        'manager_location_longitude' : 6.536313299999961
            # Zernike
    },
    {
        'id' : 2,
        'manager_url' : 'http://127.0.0.1:5002',
        'manager_location_latitude' : 10.0,
        'manager_location_longitude' : 10.0
    },
    {
        'id' : 3,
        'manager_url' : 'http://127.0.0.1:5003',
        'manager_location_latitude' : 50.0,
        'manager_location_longitude' : 6.0
    }
]
        
@app.route('/managers', methods=['GET'])
def get_managers():
    return jsonify({'managers': managers})

@app.route('/managers', methods=['POST'])
def create_manager():
    if not request.json or not 'manager_url' in request.json or not 'manager_location_latitude' in request.json or not 'manager_location_longitude' in request.json:
        abort(400)
    manager = {
        'id': managers[-1]['id'] + 1,
        'manager_url' : request.json['manager_url'],
        'manager_location_latitude' : request.json['manager_location_latitude'],
        'manager_location_longitude' : request.json['manager_location_longitude']
        }
    managers.append(manager)
    return jsonify({'manager': manager}), 201

@app.route('/managers/<string:manager_url>', methods=['DELETE'])
def delete_manager(manager_id):
    manager = [manager for manager in managers if manager['id'] == manager_id]
    if len(manager) == 0:
        abort(404)
    managers.remove(manager[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)






# curl -i -H "Content-Type: application/json" -X POST -d '{"manager_url":"bla.nl", "manager_location":"1.0 , 1.0"}' http://localhost:5000/managers









