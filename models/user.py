import uuid
from datetime import datetime
from models.review import Review
from models.place import Place
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class User:
    """
    User class represents a user in the system.
    """
    users = {} # Dictionary to store all users

    def __init__(self, email, password, first_name, last_name, city_id=None, country_id=None):
        """
        Initialize a new User instance.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            country (str, optional): The user's country. Defaults to None.
            city (str, optional): The user's city. Defaults to None.
        """
        if email in User.users:
            raise ValueError("User with email {} already exists".format(email))
        self.id = uuid.uuid4()
        self.created_at = datetime.now() 
        self.updated_at = datetime.now()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.country_id = country_id
        self.city_id = city_id
        self.places = [] # List of places hosted by the user
        self.reviews = [] # List of reviews made by the user
        User.users[email] = self # Add the user to the dictionary
        data_manager.save(self) # Save the user to the data manager
    
    def add_place(self, place):
        if place is not None:
            self.places.append(place) 
            data_manager.save(self)
            data_manager.save(place)
            print(f"Added place: {place} to user: {self.id}, user places: {self.places}")

    def add_review(self, review):
        if isinstance(review, str):
            review = Review.load(review)
        self.reviews.append(review)
        data_manager.save(self)
        data_manager.save(review)

    def update_profile(self, email=None, password=None, first_name=None, last_name=None, 
                       city_id=None, country_id=None):
        """
        Update the user's profile.

        Args:
            email (str, optional): The new email. Defaults to None.
            password (str, optional): The new password. Defaults to None.
            first_name (str, optional): The new first name. Defaults to None.
            last_name (str, optional): The new last name. Defaults to None.
            country (str, optional): The new country. Defaults to None.
            city (str, optional): The new city. Defaults to None.
        """
        if email and email != self.email and email in User.users:
            raise ValueError("User with email {} already exists".format(email))  # Check if the new email is already in use
        if email:
            del User.users[self.email] # Remove the user from the dictionary
            self.email = email  # Update the email
            User.users[self.email] = self  # Add the user back to the dictionary
        if password:
            self.password = password # Update the password
        if first_name:
            self.first_name = first_name # Update the first name
        if last_name:
            self.last_name = last_name # Update the last name
        if country_id:
            self.country_id = country_id # Update the country
        if city_id:
            self.city_id = city_id # Update the city
        self.updated_at = datetime.now()
        data_manager.save(self) # Save the updated user to the data manager


    @classmethod
    def load(cls, obj_id):
        return data_manager.load(cls, obj_id)

    @classmethod
    def load_all(cls):
        return data_manager.load_all(cls)
        
    @classmethod
    def delete(cls, obj_id):
        user = data_manager.load(cls, obj_id)
        if user:
            data_manager.delete(user)

    @classmethod
    def from_dict(cls, data):
        user = cls(
            data['email'],
            data['password'],
            data['first_name'],
            data['last_name'],
            data.get('city_id'),
            data.get('country_id')
        )
        user.id = uuid.UUID(data['id'])
        user.created_at = datetime.fromisoformat(data['created_at'])
        user.updated_at = datetime.fromisoformat(data['updated_at'])
        user.places = [Place.from_dict(place) for place in data.get('places', [])]
        user.reviews = [Review.from_dict(review) for review in data.get('reviews', [])]
        return user

    def serialize(self):
        print(f"Converting user to dict: {self.id}")
        print(f"User places before conversion: {self.places}")
        return {
            'id': str(self.id),
            'email': self.email,
            'password': self.password, # Do not include the password in the response, just for testing purposes
            'first_name': self.first_name,
            'last_name': self.last_name,
            'city_id': str(self.city_id) if hasattr(self, 'city_id') else None,
            'country_id': str(self.country_id) if hasattr(self, 'country_id') else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'places': [place.serialize() for place in (data_manager.load(Place, place_id) for place_id in self.places if place_id is not None) if place is not None],  # Convert Place objects to dictionaries
            'reviews': [review.serialize() for review in (data_manager.load(Review, review_id) for review_id in self.reviews if review_id is not None) if review is not None]  # Convert Review objects to dictionaries
        }
