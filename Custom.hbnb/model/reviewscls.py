from base_model import BaseModel




class Reviews(BaseModel):
    def __init__(self, text, clasification, user, rating):
        super().__init__()
        self.comment = text
        self.clasification = clasification
        self.user = user
        self.rating = rating


    def new_review(self, new_review):
        self.text = new_review
        print(f'This is your new text {self.text}')

    def new_clasification(self, new_clasification):
        self.clasification = new_clasification
        print(f'The clasification is: {self.clasification}')

    def delete_review(self):
        super().delete(self)

    def give_rating(self, rating):
        if not isinstance(rating, int) and rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        rating = self.rating
        return self.rating
