from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
from pprint import pprint


app = Flask(__name__)
api = Api(app)
CORS(app)



class JsonHandler:
    def __init__(self):
        pass

    def jread(self):
        with open('./api/data.json', encoding='utf-8') as json_data:
            data = json.load(json_data)
        return data

    def jwrite(self, entry, target):
        data = '';
        with open('./api/data.json', mode='r+', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data[target].append(entry)
            json_file.truncate(0)

        with open('./api/data.json', mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file)
        
        return data
            

class UserHandler(Resource):
    def get(self, u_name):
        data = JsonHandler()
        loaded_json = data.jread()
        for x in loaded_json["users"]:
            if x["name"] == u_name:
	            return {'resp': "true", 'role':x["role"], 'id':x["id"], 'name':x["name"], 'email':x["email"]}

class ApplicationHandler(Resource):
    def get(self):
        data = JsonHandler()
        loaded_json = data.jread()
        return {'resp': loaded_json["Applications"], 'size':len(loaded_json["Applications"])}
    
    def post(self):
        args =  request.get_json(force=True)
        user = args["user"]
        user_email = args["user_email"]
        BsTaxId = args["BsTaxId"]
        Bsname = args["Bsname"]
        Bscity = args["Bscity"]
        Bsstate = args["Bsstate"]
        requested_amount = args["requested_amount"]

        status = ""
        if int(requested_amount) < 50000:
            status = "Approved"
        if int(requested_amount) == 50000:
            status = "Undecided"
        if int(requested_amount) > 50000:
            status = "Declined"

        entry = {
            'user': user,
            'user_email': user_email,
            'BsTaxId': BsTaxId,
            'Bsname': Bsname,
            'Bscity': Bscity,
            'Bsstate': Bsstate,
            'requested_amount': requested_amount,
            'status':status
            }

        dt = JsonHandler()
        res_json = dt.jwrite(entry, "Applications")

        return res_json, 201

api.add_resource(UserHandler, '/v1/getUser/<string:u_name>')
api.add_resource(ApplicationHandler, '/v1/getApplications', '/v1/postApplication')

if __name__ == '__main__':
    app.run(debug=True)