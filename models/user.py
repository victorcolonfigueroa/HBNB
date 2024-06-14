from models.base_model import BaseModel
from models.place import Place
from models.review import Review

class User(BaseModel):
    """
    Represents a user with an email, password, first name, last name, city ID, country ID, places, and reviews.
    """

    user_email = {} # class variable to store email to user mapping

    def __init__(self, email, password, first_name, last_name, city_id=None, country_code=None, *args, **kwargs):
        """
        Initialize the User with an email, password, first name, last name, optional city ID, optional country ID, and optional arguments.

        :param email: The email of the user
        :param password: The password of the user
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param city_id: The city ID of the user
        :param country_id: The country ID of the user
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.city_id = city_id
        self.country_code = country_code
        self.places = [] # list of places associated with the user
        self.reviews = [] # list of reviews associated with the user
        User.user_email[email] = self
        self.save()

    @classmethod
    def unique_email(cls, email):
        """
        Check if an email is unique among all users.

        :param email: The email to check
        :return: True if the email is unique, False otherwise
        """
        users = cls.load_all()
        return not any(user.email == email for user in users)

    def add_place(self, place):
        """
        Add a place to the user. If the place is not already associated with the user, it is added.

        :param place: The place to add, either as a Place object or a string ID
        """
        if isinstance(place, str):
            place = Place.load(place)
        if place and place not in self.places:
            self.places.append(place)
            self.save()
            place.save()

    def add_review(self, review):
        """
        Add a review to the user. If the review is not already associated with the user, it is added.

        :param review: The review to add, either as a Review object or a string ID
        """
        if isinstance(review, str):
            review = Review.load(review)
        if review and review not in self.reviews:
            self.reviews.append(review)
            self.save()
            review.save()  

    def update_details(self, email=None, password=None, first_name=None, last_name=None, city_id=None, country_code=None):
        """
        Update the details of the user.

        :param email: The new email of the user
        :param password: The new password of the user
        :param first_name: The new first name of the user
        :param last_name: The new last name of the user
        :param city_id: The new city ID of the user
        :param country_id: The new country ID of the user
        """
        if email:
            self.email = email
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if city_id:
            self.city_id = city_id
        if country_code:
            self.country_code = country_code
        self.save()

    def to_dict(self):
        """
        Convert the User to a dictionary.

        :return: The User as a dictionary
        """
        data = super().to_dict()
        data.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'city_id': str(self.city_id) if hasattr(self, 'city_id') and self.city_id else None,
            'country_code': self.country_code if hasattr(self, 'country_code') and self.country_code else None,
            'places': [place.to_dict() for place in self.places if isinstance(place, Place)],
            'reviews': [review.to_dict() for review in self.reviews if isinstance(review, Review)]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create a User from a dictionary.

        :param data: The dictionary to create the User from
        :return: The created User
        """
        user = cls(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            city_id=data.get('city_id'),
            country_code=data.get('country_code'),
            id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        user.places = [Place.from_dict(place) if isinstance(place, dict) else place for place in data.get('places', [])]
        user.reviews = [Review.from_dict(review) if isinstance(review, dict) else review for review in data.get('reviews', [])]
        return user
