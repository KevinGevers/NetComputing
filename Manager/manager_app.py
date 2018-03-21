from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to the managers RESTfull webservice'


if __name__ == '__main__':
    app.run()
