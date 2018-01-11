from flask import Flask, render_template
from flask_socketio import SocketIO
import json

from flask_restful import Resource, Api
from flask_cors import CORS

from time import sleep
from threading import Thread

THREAD = Thread()

APP = Flask(__name__)
SOCKETIO = SocketIO(APP)
api = Api(APP)

cors = CORS(APP, resources={r"/*": {"origins": "*"}})

class CountThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1
        super(CountThread, self).__init__()

    def get_data(self):
        count = 0
        with open('data.json', 'r') as inpfile:
            data = json.load(inpfile)
            for i in data:
                SOCKETIO.emit('count', {'count': i}, namespace='/flask-socketio-demo')
                sleep(self.delay)
            
    def run(self):
        """Default run method"""
        self.get_data()


@APP.route('/')
def index():
    return render_template("test.html")

class sensorTypes(Resource):
    def get(self):
        with open('sensor.json', 'r') as inpfile:
            data = json.load(inpfile)
        return data

class sensorData(Resource):
    def get(self):
        with open('data.json', 'r') as inpfile:
            data = json.load(inpfile)
        return data

api.add_resource(sensorTypes, '/sensorTypes')
api.add_resource(sensorData, '/sensorData')

@SOCKETIO.on('connect', namespace='/flask-socketio-demo')
def connect_socket():
    global THREAD
    print("hello4")

    # Start thread
    if not THREAD.isAlive():
        THREAD = CountThread()
        THREAD.start()


if __name__ == '__main__':
    SOCKETIO.run(APP)
