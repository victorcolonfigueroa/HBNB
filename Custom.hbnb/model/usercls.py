from reviewscls import Reviews
from countrycls import Country, City
from placescls import Places, Amenities
from base_model import BaseModel


class User(BaseModel):
    used_emails = set()

    users = []

    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        '''self.__user_id = uuid.self.uuid4()'''
        self.first_name = first_name
        self.last_name = last_name
        self.__email = email
        User.used_emails.add(email)
        self.__password = password
        self.reviews = []

    def __dict__(self):
        return {
            'first name': self.first_name,
            'last name': self.last_name,
            'email': self.__email,
            'user ID': self.__user_id
        }

    def new_name(self, new_name, last_name):
        self.first_name = new_name
        self.last_name = last_name
        print(f"New name has been saved as {self.first_name}")

    def new_email(self, new_email):
        if new_email in User.used_emails:
            raise ValueError("Email already in use.")
        User.used_emails.remove(self.__email)
        self.__email = new_email
        print(f"New email has been saved as {self.__email}")

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password
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
