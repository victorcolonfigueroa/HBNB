from flask import Flask, request, jsonify, abort #type: ignore
from flask_restx import #look for what you have to import
import API
from model.reviewscls import Reviews
from model.placescls import Places
from model.usercls import User


def setup_route(app):
    app = Flask(__name__)

    @app.route('/places/<place_id>', methods=['POST'])
    def create_review():
        pass

    @app.route('/users/<user_id>/reviews', methods=['GET'])
    def get_reviews_form_user():
        pass

    @app.route('/places/<place_id>/reviews', methods=['GET'])
    def get_reviews_form_place():
        pass

    @app.route('/reviews/<review_id>', methods=['GET'])
    def get_reviews():
        pass

    @app.route('/reviews/<review_id>', methods=['PUT'])
    def Update_review():
        pass

    @app.route('/reviews/<review_id>', method=['DELETE'])
    def delete_review():
        pass
