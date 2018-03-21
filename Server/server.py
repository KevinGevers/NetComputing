from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to the managers RESTfull webservice'


@app.route('/managers', method='GET')
def getManagers()



# list of managers
# [[manager_url, manager_location]]
managers = [[1, ]]

if __name__ == '__main__':
    app.run()
