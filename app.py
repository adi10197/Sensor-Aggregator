from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

class sensorData(Resource):
    def get(self):
        with open('data.json', 'r') as inpfile:
            data = json.load(inpfile)
        return data

class sensorTypes(Resource):
    def get(self):
        with open('sensor.json', 'r') as inpfile:
            data = json.load(inpfile)
        return data

api.add_resource(sensorData, '/sensorData')
api.add_resource(sensorTypes, '/sensorTypes')
if __name__ == '__main__':
    app.run(debug=True)
