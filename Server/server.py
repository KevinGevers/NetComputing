from flask import Flask
from flask import make_response
from flask import request

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

managers = [{
        'manager_url' = 'test.nl'
        'manager_location' = '(0.0 , 0.0)'
        },
        {
        'manager_url' = 'test2.nl'
        'manager_location' = '(10.0 , 10.0)'
        }]

@app.route('/')
def hello_world():
    return 'Welcome to the server'


@app.route('/managers', method=['GET'])
def getManagers()
    return jsonify({'managers': managers})
    
@app.route('/managers', methods=['POST'])
def create_manager():
    if not request.json or not 'manager_url' in request.json or not 'manager_location' in request.json:
        abort(400)
    manager = {
        'manager_url' = 'test.nl'
        'manager_location' = '(0.0 , 0.0)'
        }
    managers.append(manager)
    return jsonify({'manager': manager}), 201


if __name__ == '__main__':
    app.run()
