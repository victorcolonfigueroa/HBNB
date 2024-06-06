from reviewscls import Reviews
from countrycls import Country, City
from placescls import Places, Amenities
from base_model import BaseModel
import uuid


class User(BaseModel):
    used_emails = set()

    users = []

    def __init__(self, name, email, password):
        new_user = User(name, email, password)
        if new_user in User.users:
            raise ValueError("User is already exists.")
        if email in User.used_emails:
            raise ValueError("Email already in use.")
        self.__user_id = uuid.self.uuid4()
        self.name = name
        self.__email = email
        User.used_emails.add(email)
        self.password = password
        self.reviews = []

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.__email,
            'user ID': self.__user_id
        }

    def new_name(self, new_name):
        self.name = new_name
        print(f"New name has been saved as {self.name}")

    def new_email(self, new_email):
        if new_email in User.used_emails:
            raise ValueError("Email already in use.")
        User.used_emails.remove(self.__email)
        self.__email = new_email
        print(f"New email has been saved as {self.__email}")

    def change_password(self, new_password):
        self.password = new_password
        print(f'New password has been saved')

    def add_place(self, place_name, city_name, country_name, amenities_list):
        self.place = Places(place_name)
        self.city = City(city_name)
        self.country = Country(country_name)
        self.amenities = Amenities(amenities_list)

    def add_review(self, review):
        self.review = Reviews(review)

    def get_user_info():
        info = get_user()
        return info

    def print_review_text(self):
        if hasattr(self, 'review'):
            print(self.review.text)
        else:
            print("No review has been added yet.")
