from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review

ns_place = Namespace('places', description='Place operations')

# Define the model for a place
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
    'reviews': fields.List(fields.Nested(ns_place.model('Review', {
        'id': fields.String(readOnly=True, description='The unique identifier of a review'),
        'comment': fields.String(required=True, description='The review text'),
        'rating': fields.Integer(required=True, description='The review rating'),
        'user_id': fields.String(required=True, description='The user ID'),
        'place_id': fields.String(required=True, description='The place ID'),
        'created_at': fields.DateTime(readOnly=True, description='The date and time the review was created'),
        'updated_at': fields.DateTime(readOnly=True, description='The date and time the review was last updated')
    }))),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the place was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the place was last updated')
}) 

def validate_place_data(data):
    """
    Validate the data for a place. If any of the data is invalid, abort with a 400 status code.

    :param data: The data to validate
    """
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        abort(400, description="Place name must be a non-empty string")
    if 'description' not in data or not isinstance(data['description'], str) or not data['description'].strip():
        abort(400, description="Description must be a non-empty string")
    if 'address' not in data or not isinstance(data['address'], str) or not data['address'].strip():
        abort(400, description="Address must be a non-empty string")
    if 'city_id' not in data or not isinstance(data['city_id'], str):
        abort(400, description="City ID must be provided and must be a string")
    if 'latitude' not in data or not isinstance(data['latitude'], float):
        abort(400, description="Latitude must be a float")
    if 'longitude' not in data or not isinstance(data['longitude'], float):
        abort(400, description="Longitude must be a float")
    if 'host_id' not in data or not isinstance(data['host_id'], str):
        abort(400, description="Host ID must be provided and must be a string")
    if 'number_of_rooms' not in data or not isinstance(data['number_of_rooms'], int):
        abort(400, description="Number of rooms must be an integer")
    if 'number_of_bathrooms' not in data or not isinstance(data['number_of_bathrooms'], int):
        abort(400, description="Number of bathrooms must be an integer")
    if 'price_per_night' not in data or not isinstance(data['price_per_night'], float):
        abort(400, description="Price per night must be a float")
    if 'max_guests' not in data or not isinstance(data['max_guests'], int):
        abort(400, description="Max guests must be an integer")
    if 'amenity_ids' not in data or not isinstance(data['amenity_ids'], list):
        abort(400, description="Amenity IDs must be provided and must be a list")

@ns_place.route('/')
class PlaceList(Resource):
    """
    Resource for getting a list of all places and creating new places.
    """
    @ns_place.doc('list_places')
    @ns_place.marshal_list_with(place_model)
    def get(self):
        """
        Get a list of all places.

        :return: A list of all places
        """
        places = Place.load_all()
        return [place.to_dict() for place in places]

    @ns_place.doc('create_place')
    @ns_place.expect(place_model)
    @ns_place.marshal_with(place_model, code=201)
    def post(self):
        """
        Create a new place.

        :return: The created place
        """
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_place_data(data)
        
        # Create a new Place object from the request data
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
            amenity_ids=data['amenity_ids']
        )

        host = User.load(place.host_id)
        if host:
            host.add_place(place) # Add the place to the host's list of places
        return place.to_dict(), 201

@ns_place.route('/<string:place_id>')
@ns_place.response(404, 'Place not found')
@ns_place.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """
    Resource for getting, updating, and deleting a single place.
    """
    @ns_place.doc('get_place')
    @ns_place.marshal_with(place_model)
    def get(self, place_id):
        """
        Get a single place.

        :param place_id: The ID of the place to get
        :return: The place
        """
        place = Place.load(place_id) # Load the place from the database
        if not place:
            abort(404, description="Place not found")
        return place.to_dict()

    @ns_place.doc('update_place')
    @ns_place.expect(place_model)
    @ns_place.marshal_with(place_model)
    def put(self, place_id):
        """
        Update a single place.

        :param place_id: The ID of the place to update
        :return: The updated place
        """
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")
        
        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json

        if data.get('host_id') and place.host_id and place.host_id != data['host_id']: # Check if the place already has a host
            abort(400, description="Listing already has a host")

        # Only update the fields that are present in the request data
        for key in data.keys():
            if hasattr(place, key):
                setattr(place, key, data[key])

        place.save()
        return place.to_dict()

    @ns_place.doc('delete_place')
    @ns_place.response(204, 'Place deleted')
    def delete(self, place_id):
        """
        Delete a single place.

        :param place_id: The ID of the place to delete
        """
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")

        Place.delete(place_id)
        return '', 204
