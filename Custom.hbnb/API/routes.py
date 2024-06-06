from flask import Flask, requests, jsonify, abort # type: ignore
from model.usercls import User
'''Add more routes for places reviews and verification'''

app = Flask(__name__)


def setup_routes(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        data = requests.get_json()
        user = User(data['name'], data['email'], data['password'])
        User.users.add(user)

        #Save the user to the database
        return jsonify(user.to_dict()), 201

    @app.route('/users', methods=['GET'])
    def get_all_users():
        return jsonify([user.to_dict() for user in User.users]), 200

    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        return jsonify(user.to_dict()), 200

    @app.route('/users/<user_id>', methods=['PUT'])
    def update_user(user_id):
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        data = requests.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        # Save the updated user to the database...
        return jsonify(user.to_dict()), 200

    @app.route('/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = next((user for user in User.users if user.user_id == user_id), None)
        if user is None:
            abort(404, description="User not found")
        # Delete the user from the database...
        User.users.remove(user)
        return '', 204

