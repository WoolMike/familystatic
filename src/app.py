"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['POST'])
def handle_add_member():
     body = request.get_json()  # Get the request body content
     if body is None:
        return "The request body is null", 400
     if 'first_name' not in body:
        return 'You need to specify the first_name', 400
     if 'age' not in body:
        return 'You need to specify the age', 400
     if 'lucky_numbers' not in body:
        return 'You need to specify the lucky_numbers', 400
     add_member=jackson_family.add_member(body)
    
     return jsonify(add_member), 200
     

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int:id_member>',methods=['DELETE'])
def handle_delete_member(id_member):
    member=jackson_family.delete_member(id_member)

    if member is None:
       return jsonify({'err':'member not found'}), 404
    
    

    return jsonify(member), 200

@app.route('/members/<int:id_member>',methods=['GET'])
def handle_get_member(id_member):
    member=jackson_family.get_member(id_member)

    if member is None:
       return jsonify({'err':'member not found'}), 404
    
    response=member

    return jsonify(response), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
    app.run(host='0.0.0.0', port=PORT, debug=True)