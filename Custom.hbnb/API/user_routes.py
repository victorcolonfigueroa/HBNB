from flask import Flask, requests, jsonify, abort # type: ignore
from model.usercls import User
'''RESTful endpoints for User class.'''

app = Flask(__name__)


def setup_routes(app):
    '''This function sets up endpoints for User

    Args:
        app (function): Initializes Flask

    Returns:
        string: returns a list in json format depending on the method
    '''
    @app.route('/users', methods=['POST'])
    def create_user():
        '''Creates user

        Returns:
            string: return a json object of user instances in json format
        '''
        data = requests.get_json()
        user = User(data['first_name'], 'last_name', data['email'], data['password'])
        User.users.add(user)

        #Save the user to the database
        return jsonify(user.to_dict()), 201

    @app.route('/users', methods=['GET'])
    def get_all_users():
        '''gets a list of users registered

        Returns:
            string: returns list of users in json object
        '''
        return jsonify([user.to_dict() for user in User.users]), 200

    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        '''gets user id

        Args:
            user_id string: string of unique id

        Returns:
            stirng: returns a string of user id
        '''
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        return jsonify(user.to_dict()), 200

    @app.route('/users/<user_id>', methods=['PUT'])
    def update_user(user_id):
        '''updates user information

        Args:
            user_id (string): unique id of the user

        Returns:
            list: Returns a list with the updated user information
        '''
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        data = requests.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        # Save the updated user to the database...
        return jsonify(user.to_dict()), 200

    @app.route('/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        '''deletes the user profile

        Args:
            user_id (string): unique id of user

        Returns:
            string: returns a blank string meaning it succesfully deleted the user
        '''
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        # Delete the user from the database...
        User.users.remove(user)
        return '', 204

