from models.review import Review
from flask import request, abort
from flask_restx import Namespace, Resource, fields
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from models.user import User
from models.place import Place
from datetime import datetime

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

ns_review = Namespace('reviews', description='Review operations')

review_model = ns_review.model('Review', {
    'id': fields.String(readOnly=True, description='The unique identifier of a review'),
    'text': fields.String(required=True, description='The review text'),
    'rating': fields.Integer(required=True, description='The review rating'),
    'user_id': fields.String(required=True, description='The user ID'),
    'place_id': fields.String(required=True, description='The place ID'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the review was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the review was last updated')
})

def validate_review_data(data):
    if 'text' not in data or not isinstance(data['text'], str) or not data['text'].strip():
        abort(400, description="Review text must be a non-empty string")
    if 'rating' not in data or not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
        abort(400, description="Rating must be an integer between 1 and 5")
    user = User.load(data['user_id'])
    if not user:
        abort(400, description="Invalid user ID")
    place = Place.load(data['place_id'])
    if not place:
        abort(400, description="Invalid place ID")
    if place.host_id == data['user_id']:
        abort(400, description="Hosts cannot review their own places")

@ns_review.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @ns_review.doc('list_reviews_for_place')
    @ns_review.marshal_list_with(review_model)
    def get(self, place_id):
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")
        return [review.to_dict() for review in place.reviews]

    @ns_review.doc('create_review_for_place')
    @ns_review.expect(review_model)
    @ns_review.marshal_with(review_model, code=201)
    def post(self, place_id):
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        data['place_id'] = place_id
        validate_review_data(data)
        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=data['user_id'],
            place_id=place_id
        )
        user = User.load(data['user_id'])
        user.add_review(review)
        place = Place.load(place_id)
        place.add_review(review)

@ns_review.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    @ns_review.doc('list_reviews_for_user')
    @ns_review.marshal_list_with(review_model)
    def get(self, user_id):
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")
        return [Review.load(review).to_dict() for review in user.reviews]

@ns_review.route('/reviews/<string:review_id>')
@ns_review.response(404, 'Review not found')
@ns_review.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @ns_review.doc('get_review')
    @ns_review.marshal_with(review_model)
    def get(self, review_id):
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")
        return review.to_dict()

    @ns_review.doc('update_review')
    @ns_review.expect(review_model)
    @ns_review.marshal_with(review_model)
    def put(self, review_id):
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            review.rating = data['rating']
        review.updated_at = datetime.now()
        data_manager.save(review)
        return review.to_dict()

    @ns_review.doc('delete_review')
    @ns_review.response(204, 'Review deleted')
    def delete(self, review_id):
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")

        Review.delete(review_id)
        return '', 204
