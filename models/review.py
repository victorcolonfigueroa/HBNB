import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Review:
    """
    Review class represents a review in the system.
    """
    reviews = [] # List of all reviews in the system

    def __init__(self, text, rating, user_id, place_id):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        data_manager.save(self)

    def update_details(self, text=None, rating=None):
        if text:
            self.text = text
        if rating:
            self.rating = rating
        self.updated_at = datetime.now()
        data_manager.save(self)

    @classmethod
    def load(cls, obj_id):
        return data_manager.load(cls, obj_id)

    @classmethod
    def load_all(cls):
        return data_manager.load_all(cls)

    @classmethod
    def delete(cls, obj_id):
        review = data_manager.load(cls, obj_id)
        if review:
            data_manager.delete(review)

    @classmethod
    def from_dict(cls, data):
        review = cls(data['text'], data['rating'], data['user_id'], data['place_id'])
        review.id = uuid.UUID(data['id'])
        review.created_at = datetime.fromisoformat(data['created_at'])
        review.updated_at = datetime.fromisoformat(data['updated_at'])
        return review

    def to_dict(self):
        return {
            'id': str(self.id),
            'text': self.text,
            'rating': self.rating,
            'user_id': str(self.user_id),
            'place_id': str(self.place_id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
