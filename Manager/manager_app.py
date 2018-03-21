from flask import Flask, jsonify

app = Flask(__name__)

parking_spaces = {
    'total' : 20,
    'availible' : 5,
    'reserved' : 2
}

@app.route('/parkingspaces', methods=['GET'])
def get_parkingspaces():
    return jsonify(parking_spaces)

if __name__ == '__main__':
    app.run(debug=True)
