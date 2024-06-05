from reviewscls import Reviews
from countrycls import Country, City
from placescls import Places, Amenities
import uuid


class User:
    used_emails = set()

    def __init__(self, name, email, password):
        if email in User.used_emails:
            raise ValueError("Email already in use.")
        self.user_id = uuid.self.uuid4()
        self.name = name
        self.email = email
        User.used_emails.add(email)
        self.password = password
        self.reviews = []

    def new_name(self, new_name):
        self.name = new_name
        print(f"New name has been saved as {self.name}")

    def new_email(self, new_email):
        if new_email in User.used_emails:
            raise ValueError("Email already in use.")
        User.used_emails.remove(self.email)
        self.email = new_email
        print(f"New email has been saved as {self.email}")

    def new_password(self, new_password):
        self.password = new_password
        print(f'New password has been saved')

    def add_place(self, place_name, city_name, country_name, amenities_list):
        self.place = Places(place_name)
        self.city = City(city_name)
        self.country = Country(country_name)
        self.amenities = Amenities(amenities_list)

    def add_review(self, review):
        self.review = Reviews(review)

    def print_review_text(self):
        if hasattr(self, 'review'):
            print(self.review.text)
        else:
            print("No review has been added yet.")
