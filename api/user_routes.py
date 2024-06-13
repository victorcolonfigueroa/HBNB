from flask import request, jsonify, abort, Blueprint
from flask_restx import Api, Namespace, Resource, fields
from models.user import User
from models.city import City
from models.country import Country
from models.place import Place
from werkzeug.security import generate_password_hash

ns_user = Namespace('users', description='User operations')

# Define the model for a user
user_model = ns_user.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'city_id': fields.String(description='The city ID'),
    'country_id': fields.String(description='The country ID'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the user was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the user was last updated'),
    'places': fields.List(fields.Nested(ns_user.model('Place', {
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
    }))),
    'reviews': fields.List(fields.Nested(ns_user.model('Review', {
        'id': fields.String(readOnly=True, description='The unique identifier of a review'),
        'comment': fields.String(required=True, description='The review text'),
        'rating': fields.Integer(required=True, description='The review rating'),
        'user_id': fields.String(required=True, description='The user ID'),
        'place_id': fields.String(required=True, description='The place ID'),
        'created_at': fields.DateTime(readOnly=True, description='The date and time the review was created'),
        'updated_at': fields.DateTime(readOnly=True, description='The date and time the review was last updated')
    })))
})


def validate_email(email):
    """
    Validates an email address using a regular expression.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        A match object if the email address is valid, None otherwise.
    """
    import re
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # Regular expression for validating email addresses
    return re.match(email_regex, email) # Return a match object if the email address is valid, None otherwise

def validate_user_data(data):
    """
    Validates the user data. If any of the data is invalid, abort with a 400 status code.

    :param data: The data to validate
    """
    if 'email' not in data or not isinstance(data['email'], str) or not data['email'].strip():
        abort(400, description="Email must be a non-empty string")
    if 'password' not in data or not isinstance(data['password'], str) or not data['password'].strip():
        abort(400, description="Password must be a non-empty string")
    if 'first_name' not in data or not isinstance(data['first_name'], str) or not data['first_name'].strip():
        abort(400, description="First name must be a non-empty string")
    if 'last_name' not in data or not isinstance(data['last_name'], str) or not data['last_name'].strip():
        abort(400, description="Last name must be a non-empty string")
    if 'city_id' in data:
        city = City.load(data['city_id'])
        if not city:
            abort(400, description="Invalid city ID")
    if 'country_id' in data:
        country = Country.load(data['country_id'])
        if not country:
            abort(400, description="Invalid country ID")

@ns_user.route('/')
class UserList(Resource):
    """
    Resource for getting a list of all users and creating new users.
    """
    @ns_user.doc('list_users')
    @ns_user.marshal_list_with(user_model)
    def get(self):
        """
        Get a list of all users.

        :return: A list of all users
        """
        users = User.load_all()
        return [user.to_dict() for user in users]

    @ns_user.doc('create_user')
    @ns_user.expect(user_model)
    @ns_user.marshal_with(user_model, code=201)
    def post(self):
        """
        Create a new user.

        :return: The created user
        """
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_user_data(data)
        # Check if the email address is already in use
        if not User.unique_email(data['email']):
            abort(400, description="Email address is already in use")
        # Hash the password before storing it
        hashed_password = generate_password_hash(data['password'])
        # Create the user
        user = User(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            city_id=data.get('city_id'),
            country_id=data.get('country_id')
        )
        return user.to_dict(), 201

@ns_user.route('/<string:user_id>')
@ns_user.response(404, 'User not found')
@ns_user.param('user_id', 'The user identifier')
class UserResource(Resource):
    """
    Resource for getting, updating, and deleting a single user.
    """
    @ns_user.doc('get_user')
    @ns_user.marshal_with(user_model)
    def get(self, user_id):
        """
        Get a single user.

        :param user_id: The ID of the user to get
        :return: The user
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")
        return user.to_dict()

    @ns_user.doc('update_user')
    @ns_user.expect(user_model)
    @ns_user.marshal_with(user_model)
    def put(self, user_id):
        """
        Update a single user.

        :param user_id: The ID of the user to update
        :return: The updated user
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_user_data(data)
        user.update_details(
            email=data.get('email'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            city_id=data.get('city_id'),
            country_id=data.get('country_id')
        )
        return user.to_dict()

    @ns_user.doc('delete_user')
    @ns_user.response(204, 'User deleted')
    def delete(self, user_id):
        """
        Delete a single user.

        :param user_id: The ID of the user to delete
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")

        User.delete(user_id)
        return '', 204
