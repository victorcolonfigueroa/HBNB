import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from Base_model import BaseModel

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Review(BaseModel):
    """
    Review class represents a review in the system.
    """
    def __init__(self, user, place, rating, comment):
        """
        Initialize a new Review instance.

        Args:
            user (User): The user who wrote the review.
            place (Place): The place that the review is for.
            rating (int): The rating given by the user.
            comment (str): The comment written by the user.
        """
        super().__init__()
        self.user = user
        self.place = place
        self.rating = rating
        self.comment = comment
        data_manager.save(self) # Save the review to the data manager

    def update_review(self, rating=None, comment=None):
        """
        Update the review's rating and comment.

        Args:
            rating (int, optional): The new rating. Defaults to None.
            comment (str, optional): The new comment. Defaults to None.
        """
        if rating:
            self.rating = rating # Update the rating
        if comment:
            self.comment = comment # Update the comment
        self.updated_at = datetime.now() # Update the updated_at timestamp
        data_manager.save(self) # Save the updated review to the data manager

    @classmethod
    def load(cls, obj_id):
        """
        Load a review by ID.

        Args:
            obj_id (uuid.UUID): The ID of the review to be loaded.

        Returns:
            Review: The loaded review.
        """
        return data_manager.load(cls, obj_id) # Load the review with the given id

    @classmethod
    def load_all(cls):
        """
        Load all reviews.

        Returns:
            list: A list of all reviews.
        """
        return data_manager.load_all(cls) # Load all reviews from the data manager

    @classmethod
    def delete(cls, obj_id):
        """
        Delete a review by ID.

        Args:
            obj_id (uuid.UUID): The ID of the review to be deleted.
        """
        review = data_manager.load(cls, obj_id) # Load the review with the given id
        if review: # Check if the review exists
            data_manager.delete(review) # Delete the review from the data manager
