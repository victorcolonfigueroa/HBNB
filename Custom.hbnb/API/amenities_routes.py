from flask import Flask, requests, jsonify #type: ignore
from model.placescls import Amenities
import uuid

app = Flask(__name__)

def setup_routes(app):

    @app.route('/amenities', methods= ['GET'])
    def get_amenities():
        amenities = Amenities.load_all()
        return jsonify([amenity.__dict__ for amenity in amenities])

    @app.route('/amenities', methods=['POST'])
    def create_amenity():
        data = requests.get_json()
        new_amenitie = Amenities(data['name'], data['description'])
        return jsonify(new_amenitie.__dict__), 201

    @app.route('/amenity/<amenity_id>', methods=['PUT'])
    def update_amenity(amenity_id):
        data = requests.get_json()
        amenity = Amenities.get(uuid.UUID(amenity_id))
        if 'name' in data:
            amenity.name = data['name']
        if 'description' in data:
            amenity.description = data['description']
        amenity.save()
        return jsonify(amenity.__dict__), 200

    @app.route('/ameniteis/<amenity_id>', methods=['DELETE'])
    def delete_amenity(amenity_id):
        Amenities .delete(uuid.UUID(amenity_id))
        return'',204

if __name__ == '__main__':
    app.run(debug=True)
