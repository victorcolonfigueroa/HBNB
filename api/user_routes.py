from flask import request, jsonify, abort, Blueprint
from flask_restx import Api, Namespace, Resource, fields
from models.user import User
from werkzeug.security import generate_password_hash
from api import api

# Define a model for the User object
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='The user email'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'password': fields.String(required=True, description='The user password'),
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
    Validates user data. Checks if the email, first name, and last name are present and valid.
    
    Args:
        data (dict): The user data to validate.
        
    Raises:
        HTTPException: If the email, first name, or last name are not valid.
    """
    if 'email' not in data or not validate_email(data['email']):
        abort(400, description="Invalid email format")
    if 'first_name' not in data or not isinstance(data['first_name'], str) or not data['first_name'].strip():
        abort(400, description="First name must be a non-empty string")
    if 'last_name' not in data or not isinstance(data['last_name'], str) or not data['last_name'].strip():
        abort(400, description="Last name must be a non-empty string")

# Define a Flask blueprint
blueprint = Blueprint('api', __name__)

# Initialize the API with the blueprint
api = Api(blueprint)

# Define a namespace
ns_user = Namespace('users', description='User operations')

# Add the namespace to the API
api.add_namespace(ns_user)

@ns_user.route('/')
class UserList(Resource):
    """
    Resource for handling the HTTP methods for the /users route.
    """
    def get(self):
        """
        Returns a list of all users.
        
        Returns:
            A JSON array of users.
        """
        users = User.load_all()
        return jsonify([user.__dict__ for user in users]) # Return a JSON array of user dictionaries

    def post(self):
        """
        Creates a new user with the data provided in the request.
        
        Returns:
            The created user as JSON, with a status code of 201.
            
        Raises:
            HTTPException: If the request payload is not JSON, the user data is not valid, or the email already exists.
        """
        if not request.json:
            abort(400, description="Request payload must be JSON") # Return a 400 Bad Request response if the request payload is not JSON
        data = request.json # Get the JSON data from the request
        validate_user_data(data) # Validate the user data
        
        email = data['email'] # Get the email from the data
        password = data.get('password', "") # Get the password from the data, default to an empty string if not present
        first_name = data['first_name'] # Get the first name from the data
        last_name = data['last_name'] # Get the last name from the data
        
        users = User.load_all()
        if users:
            for user in users:
                if user.email == email:
                    abort(409, description="Email already exists")
        
        try:
            # Create a new user with the provided data
            hashed_password = generate_password_hash(password) # Hash the password
            user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
            return jsonify(user=user.serialize()), 201 # Return the user as JSON with a status code of 201
        except ValueError as e:
            abort(400, description=str(e))

@ns_user.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for handling the HTTP methods for the /users/<user_id> route.
    """
    def get(self, user_id):
        """
        Returns the user with the given ID.
        
        Args:
            user_id (str): The ID of the user to return.
            
        Returns:
            The user as JSON.
            
        Raises:
            HTTPException: If the user is not found.
        """
        user = User.load(user_id) # Load the user with the given ID
        if not user:
            abort(404, description="User not found") # Return a 404 Not Found response if the user is not found
        return jsonify(user.__dict__)  # Return the user as JSON

    def put(self, user_id):
        """
        Updates the user with the given ID with the data provided in the request.
        
        Args:
            user_id (str): The ID of the user to update.
            
        Returns:
            The updated user as JSON.
            
        Raises:
            HTTPException: If the user is not found, the request payload is not JSON, the user data is not valid, or the email already exists.
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")
        
        if not request.json:
            abort(400, description="Request payload must be JSON")
        
        data = request.json
        validate_user_data(data)
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if email and email != user.email: # Check if the email has changed
            for u in User.load_all(): # Check if the new email already exists
                if u.email == email: # If the email already exists, return a 409 Conflict response
                    abort(409, description="Email already exists")
        
        try:
            # Update the user with the provided data
            user.update_profile(email=email, password=password, first_name=first_name, last_name=last_name)
            return jsonify(user.__dict__)
        except ValueError as e: # If there is an error updating the user, return a 400 Bad Request response
            abort(400, description=str(e))

    def delete(self, user_id):
        """
        Deletes the user with the given ID.
        
        Args:
            user_id (str): The ID of the user to delete.
            
        Returns:
            An empty response with a status code of 204.
            
        Raises:
            HTTPException: If the user is not found.
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")
        
        User.delete(user_id) # Delete the user
        return '', 204 # Return an empty response with a status code of 204
