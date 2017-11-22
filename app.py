from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class temperature(Resource):
    def get(self):
        return {'temperature': 25}

class phSensor(Resource):
    def get(self):
        return {'phSensor': 5}

api.add_resource(temperature, '/temperature')
api.add_resource(phSensor, '/phSensor')
if __name__ == '__main__':
    app.run(debug=True)
