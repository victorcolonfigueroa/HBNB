from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.review import Review
from models.place import Place
from models.user import User

ns_review = Namespace('reviews', description='Review operations')

# Define the model for a review
review_model = ns_review.model('Review', {
    'id': fields.String(readOnly=True, description='The unique identifier of a review'),
    'place_id': fields.String(required=True, description='The place ID'),
    'user_id': fields.String(required=True, description='The user ID'),
    'rating': fields.Integer(required=True, description='The rating'),
    'comment': fields.String(required=True, description='The comment'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the review was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the review was last updated')
})

def validate_review_data(data):
    """
    Validates the review data. If any of the data is invalid, abort with a 400 status code.

    :param data: The data to validate
    """
    if 'place_id' not in data or not isinstance(data['place_id'], str):
        abort(400, description="Place ID must be provided and must be a string")
    if 'user_id' not in data or not isinstance(data['user_id'], str):
        abort(400, description="User ID must be provided and must be a string")
    if 'rating' not in data or not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
        abort(400, description="Rating must be an integer between 1 and 5")
    if 'comment' not in data or not isinstance(data['comment'], str) or not data['comment'].strip():
        abort(400, description="Comment must be a non-empty string")

@ns_review.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource for getting a list of all reviews for a place and creating new reviews for a place.
    """
    @ns_review.doc('list_reviews_for_place')
    @ns_review.marshal_list_with(review_model)
    def get(self, place_id):
        """
        Get a list of all reviews for a place.

        :param place_id: The ID of the place to get reviews for
        :return: A list of all reviews for the place
        """
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")
        return [review.to_dict() for review in place.reviews]

    @ns_review.doc('create_review_for_place')
    @ns_review.expect(review_model)
    @ns_review.marshal_with(review_model, code=201)
    def post(self, place_id):
        """
        Create a new review for a place.

        :param place_id: The ID of the place to create a review for
        :return: The created review
        """
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_review_data(data)
        # Ensure the place ID in the path and payload match
        if place_id != data['place_id']:
            abort(400, description="Place ID in the path and payload do not match")
        place = Place.load(place_id)
        if not place:
            abort(404, description="Place not found")
        # Ensure the user ID in the payload exists
        user = User.load(data['user_id'])
        if not user:
            abort(404, description="User not found")
        # Ensure the user is not reviewing their own listing
        if place.host_id == user.id:
            abort(400, description="Hosts cannot review their own listings")
        
        # Create the review
        review = Review(
            place_id=data['place_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment']
        )
        place.add_review(review)
        user.add_review(review)
        return review.to_dict(), 201

@ns_review.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    """
    Resource for getting a list of all reviews by a user.
    """
    @ns_review.doc('list_reviews_for_user')
    @ns_review.marshal_list_with(review_model)
    def get(self, user_id):
        """
        Get a list of all reviews by a user.

        :param user_id: The ID of the user to get reviews for
        :return: A list of all reviews by the user
        """
        user = User.load(user_id)
        if not user:
            abort(404, description="User not found")
        return [review.to_dict() for review in user.reviews]

@ns_review.route('/reviews/<string:review_id>')
@ns_review.response(404, 'Review not found')
@ns_review.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """
    Resource for getting, updating, and deleting a single review.
    """
    @ns_review.doc('get_review')
    @ns_review.marshal_with(review_model)
    def get(self, review_id):
        """
        Get a single review.

        :param review_id: The ID of the review to get
        :return: The review
        """
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")
        return review.to_dict()

    @ns_review.doc('update_review')
    @ns_review.expect(review_model)
    @ns_review.marshal_with(review_model)
    def put(self, review_id):
        """
        Update a single review.

        :param review_id: The ID of the review to update
        :return: The updated review
        """
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_review_data(data)
        
        # Update the review
        review.update_details(
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        return review.to_dict()

    @ns_review.doc('delete_review')
    @ns_review.response(204, 'Review deleted')
    def delete(self, review_id):
        """
        Delete a single review.

        :param review_id: The ID of the review to delete
        """
        review = Review.load(review_id)
        if not review:
            abort(404, description="Review not found")

        Review.delete(review_id)
        return '', 204
