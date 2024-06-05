from reviewscls import Reviews
from countrycls import Country, City
from placescls import Places, Amenities
import uuid


class User:
    '''move the uuid function to make a get property that
    grabs name and email and makes a unique id with uuid4'''
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.reviews = []


    def new_name(self, new_name):
        self.name = new_name #review this function
        print(f"New name has been saved as {self.name}")

    def new_email(self, new_email): #review this function
        self.email = new_email
        print(f"New email has been saved as {self.email}")

    def new_password(self, new_password):
        self.password = new_password
        print(f'New password has been saved')

    def create_account():
        pass

    def add_review(self, review):
        if not isinstance(review, Reviews):
            raise ValueError("review must be an instance of Reviews")
        self.reviews.append(review)
        review.user = self

    def add_place(self, self.place_name, ity, ountry, menities):
        self.place = self.place_name
        self.city = self.city_name
        self.country = self.country_name
'''find a way to integrate city country amenities and place class in add_place'''
