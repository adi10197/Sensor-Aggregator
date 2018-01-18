from flask import Flask, render_template
from flask_socketio import SocketIO
import json

from flask_restful import Resource, Api
from flask_cors import CORS

from time import sleep
from threading import Thread

"""XLS -> json converter

first:
  $ pip install xlrd

then:
  $ cat in.xls
date, temp, pressure
Jan 1, 73, 455
Jan 3, 72, 344
Jan 7, 52, 100

convert:
  $ python xls_to_json.py in.xls Sheet1 out.json

finally:
  $ cat out.json
{
  'data': [
    {'date': 'Jan 1', 'temp': 73, 'pressure': 455},
    {'date': 'Jan 3', 'temp': 72, 'pressure': 344},
    {'date': 'Jan 7', 'temp': 52, 'pressure': 100},
  ]
}
"""
import json
import sys

import xlrd

def take_xls():
    workbook = xlrd.open_workbook('log.xlsx')
    worksheet = workbook.sheet_by_name('sheet1')

    data1 = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data1 = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data1[keys[col_number]] = cell.value
        data1.append(row_data1)

    return data1

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
            print(take_xls())
            for i in take_xls():
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

    # Start thread
    if not THREAD.isAlive():
        THREAD = CountThread()
        THREAD.start()


if __name__ == '__main__':
    SOCKETIO.run(APP)
