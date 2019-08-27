from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import linkk
from PIL import Image

app1 = Flask(__name__)
api = Api(app1)
l1 = linkk.linking


class Hello_world(Resource):
    def get(self, address):
        return jsonify(str=l1.run(self, address))      

api.add_resource(Hello_world, '/<string:address>')

    
if __name__ == "__main__":
    app1.run(debug=True)