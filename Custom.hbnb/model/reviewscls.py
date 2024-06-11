from base_model import BaseModel
from usercls import User
from placescls import Places



class Reviews(BaseModel):
    def __init__(self, text):
        super().__init__()
        self.comment = text
        self.rating = None
        self.place_id = None
        self.user_id = None



    def new_review(self, new_review):
        self.text = new_review
        print(f'This is your new text {self.text}')

    def delete_review(self):
        super().delete(self)

    def give_rating(self, rating):
        if not isinstance(rating, int) and rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        rating = self.rating
        return self.rating

    def assign_user(self):
        id = User.self.id
        self.user_id = super().host(self, id)

    def assign_place(self):
        id = Places.self.id
        self.place_id = super().host(self, id)
