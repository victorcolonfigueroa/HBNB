from flask import Flask, requests, jsonify
from place import Place
import uuid

app = Flask(__name__)

@app.route('/place', methods=['GET'])
def get_places():
    places = Place.load_all()
    return jsonify([place.__dict__ for place in places])

@app.route('/places', methods= (['POST']))
def create_place():
    data = requests.get_json()
    new_place = Place(data['name'], data['description'], data['price'], data['direction'])
    return jsonify(new_place.__dict__), 201

@app.route('/places/<place_id>', methods= ['PUT'])
def update_place(place_id):
    data = requests.get_json()
    palce = Place.get(uuid.UUID(place_id))
    if 'name' in data:
        place.name = data['name']
    if 'description' in data:
        place.description = data['description']
    if 'prince' in data:
        place.price = data['price']
    if 'direction' in data:
        place_directrion = data['direction']
        place.save()
        return jsonify(place.__dict__), 200
    
@app.route('/places/<place_id>', methods= ['DELETE'])
def delete_place(place_id):
    Place.delete(uuid.UUID(place_id))
    return '', 204
