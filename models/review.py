import uuid
from datetime import datetime


class Review:
    def __init__(self, user, place, rating, comment):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.user = user
        self.place = place
        self.rating = rating
        self.comment = comment


    def update_review(self, rating=None, comment=None):
        if rating:
            self.rating = rating
        if comment:
            self.comment = comment
        self.updated_at = datetime.now() 
