from models.base_model import BaseModel

class Review(BaseModel):
    """
    Represents a review with a place ID, user ID, rating, and comment.
    """

    def __init__(self, place_id, user_id, rating, comment, *args, **kwargs):
        """
        Initialize the Review with a place ID, user ID, rating, comment, and optional arguments.

        :param place_id: The ID of the place the review is for
        :param user_id: The ID of the user who wrote the review
        :param rating: The rating given in the review
        :param comment: The comment written in the review
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.review_author = None
        self.save()

    def update_details(self, rating=None, comment=None):
        """
        Update the details of the review.

        :param rating: The new rating for the review
        :param comment: The new comment for the review
        """
        if rating:
            self.rating = rating
        if comment:
            self.comment = comment
        self.save()

    def to_dict(self):
        """
        Convert the Review to a dictionary.

        :return: The Review as a dictionary
        """
        data = super().to_dict()
        data.update({
            'place_id': str(self.place_id),
            'user_id': str(self.user_id),
            'rating': self.rating,
            'comment': self.comment
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create a Review from a dictionary.

        :param data: The dictionary to create the Review from
        :return: The created Review
        """
        return cls(
            place_id=data['place_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data['comment'],
            id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
