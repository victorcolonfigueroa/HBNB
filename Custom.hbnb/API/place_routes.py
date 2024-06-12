from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity

ns_place = Namespace('places', description='Place operations')

place_model = ns_place.model('Place', {
    'id': fields.String(readOnly=True, description='The unique identifier of a place'),
    'name': fields.String(required=True, description='The place name'),
    'description': fields.String(required=True, description='The place description'),
    'address': fields.String(required=True, description='The place address'),
    'city_id': fields.String(required=True, description='The city ID'),
    'latitude': fields.Float(required=True, description='The latitude of the place'),
    'longitude': fields.Float(required=True, description='The longitude of the place'),
    'host_id': fields.String(required=True, description='The host ID'),
    'number_of_rooms': fields.Integer(required=True, description='The number of rooms in the place'),
    'number_of_bathrooms': fields.Integer(required=True, description='The number of bathrooms in the place'),
    'price_per_night': fields.Float(required=True, description='The price per night'),
    'max_guests': fields.Integer(required=True, description='The maximum number of guests'),
    'amenity_ids': fields.List(fields.String, required=True, description='The list of amenity IDs'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the place was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the place was last updated')
})

def validate_place_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        abort(400, description="Place name must be a non-empty string")
    if 'latitude' not in data or not isinstance(data['latitude'], (float, int)) or not (-90 <= data['latitude'] <= 90):
        abort(400, description="Latitude must be a valid number between -90 and 90")
    if 'longitude' not in data or not isinstance(data['longitude'], (float, int)) or not (-180 <= data['longitude'] <= 180):
        abort(400, description="Longitude must be a valid number between -180 and 180")
    if 'number_of_rooms' not in data or not isinstance(data['number_of_rooms'], int) or data['number_of_rooms'] < 0:
        abort(400, description="Number of rooms must be a non-negative integer")
    if 'number_of_bathrooms' not in data or not isinstance(data['number_of_bathrooms'], int) or data['number_of_bathrooms'] < 0:
        abort(400, description="Number of bathrooms must be a non-negative integer")
    if 'max_guests' not in data or not isinstance(data['max_guests'], int) or data['max_guests'] < 0:
        abort(400, description="Maximum number of guests must be a non-negative integer")
    if 'price_per_night' not in data or not isinstance(data['price_per_night'], (float, int)) or data['price_per_night'] < 0:
        abort(400, description="Price per night must be a valid non-negative number")
    city = City.load(data['city_id'])
    if not city:
        abort(400, description="Invalid city ID")
    host = User.load(data['host_id'])
    if not host:
        abort(400, description="Invalid host ID")
    for amenity_id in data.get('amenity_ids', []):
        amenity = Amenity.load(amenity_id)
        if not amenity:
            abort(400, description=f"Invalid amenity ID: {amenity_id}")

@ns_place.route('/')
class PlaceList(Resource):
    @ns_place.doc('list_places')
    @ns_place.marshal_list_with(place_model)
    def get(self):
        places = Place.load_all()
        return [place.to_dict() for place in places]

    @ns_place.doc('create_place')
    @ns_place.expect(place_model)
    @ns_place.marshal_with(place_model, code=201)
    def post(self):
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_place_data(data)
        city = City.load(data['city_id'])
        host = User.load(data['host_id'])
        amenities = [Amenity.load(amenity_id) for amenity_id in data['amenity_ids']]
        place = Place(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city_id=data['city_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            host_id=data['host_id'],
            number_of_rooms=data['number_of_rooms'],
            number_of_bathrooms=data['number_of_bathrooms'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            amenity_ids=[amenity.id for amenity in amenities]
        )
        host.add_place(place)  # Add place to the host's places
        return place.to_dict(), 201

@ns_place.route('/<string:place_id>')
@ns_place.response(404, 'Place not found')
@ns_place.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @ns_place.doc('get_place')
    @ns_place.marshal_with(place_model)
    def get(self, place_id):
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")
        return place.to_dict()

    @ns_place.doc('update_place')
    @ns_place.expect(place_model)
    @ns_place.marshal_with(place_model)
    def put(self, place_id):
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_place_data(data)
        city = City.load(data['city_id'])
        host = User.load(data['host_id'])
        amenities = [Amenity.load(amenity_id) for amenity_id in data['amenity_ids']]
        place.update_details(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city_id=data['city_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            host_id=data['host_id'],
            number_of_rooms=data['number_of_rooms'],
            number_of_bathrooms=data['number_of_bathrooms'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            amenity_ids=[amenity.id for amenity in amenities]
        )
        return place.to_dict()

    @ns_place.doc('delete_place')
    @ns_place.response(204, 'Place deleted')
    def delete(self, place_id):
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")

        Place.delete(place_id)
        return '', 204
