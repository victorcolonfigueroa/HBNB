from flask import Flask, request, jsonify, abort, Blueprint #type: ignore
from flask_restx import Resource, Namespace, Api, fields #type: ignore
from api import api #type: ignore
from model.reviewscls import Reviews
from model.placescls import Places
from model.usercls import User
from persistence.data_manager import DataManager #for when we merge all directories
from persistence.file_storage import FileStorage
'''finish this file ASAP!!!'''

app = Flask(__name__)
api = Api(app)

review_model = api.model('Review', {
    'user_id': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(required=True),
})
'''Add docstring and add rating function make sure you get to store
    the required fields to the classes.'''
blueprint = Blueprint('api',__name__)

api = Api(Blueprint)

ns_review = Namespace('reviews', description='users reviews of places and ratings')

api.add_namespace(ns_review)

@ns_review.route('/places')
class ReviewList(Resource):
    @ns_review.doc('list_review')
    @ns_review.marshal_list_with(review_model)
    def post(self):
        if not request.json:
            abort(400, description='Request payload must be json')
        data = request.json
        try:
            review = Reviews(comment=data['comment'], rating=data['rating'], user_id=data['user_id'])
            data_manager.save(review) #make a save method to persist the Reviews
            return review, 201
        except ValueError as e:
            abort(400, description=str(e))


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
