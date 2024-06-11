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

@ns_review.route('/places/reviews')
class ReviewList(Resource):
    @ns_review.doc('list_review')
    @ns_review.marshal_list_with(review_model)
    def post(self):
        if not request.json:
            abort(400, description='Request payload must be json')
        data = request.json
        try:
            review = Reviews(comment=data['comment'], rating=data['rating'], user_id=data['user_id'])
            data_manager.save(review)
            return review, 201
        except ValueError as e:
            abort(400, description=str(e))

    def get(self, user_id):
        review = Reviews.load_all(user_id) #make a method in review to get reviews
        return review

    def get(self, place_id):
        review = Reviews.load_all(place_id)
        return review

    def get(self, review_id):
        review = Reviews.load_all(review_id)
        return review

    def put(self, review_id):
        review = Reviews.load(review_id)
        if not review:
            abort(404, description="Review not found.")

        if not request.json:
            abort(400, description="Request payload must be json.")

        data = request.json
        validate_review_data(data)#Add this function to review

        review = data.get('review')
        reviewid = data.get('review_id')

        try:
            review = Reviews.load(review_id)
            Reviews.update(review=review)#Add rating when you make rating method
            data_manager.save(review)
            return review
        except ValueError as e:
            abort(400, descriptio=str(e))

    def delete(self, review_id):
        try:
            review = Reviews.load(review_id)
            if review is None:
                abort(404, description="Review not found.")
            review.delete(review_id)
            return '', 204
        except Exception as e:
            abort(500, description=str(e))
