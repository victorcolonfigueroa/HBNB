import uuid
from datetime import datetime
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

    def __init__(self, email, password, first_name, last_name):
        """
        Initialize a new User instance.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
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
        self.places = [] # List of places hosted by the user
        self.reviews = [] # List of reviews made by the user
        User.users[email] = self # Add the user to the dictionary
        data_manager.save(self) # Save the user to the data manager


    def update_profile(self, email=None, password=None, first_name=None, last_name=None):
        """
        Update the user's profile.

        Args:
            email (str, optional): The new email. Defaults to None.
            password (str, optional): The new password. Defaults to None.
            first_name (str, optional): The new first name. Defaults to None.
            last_name (str, optional): The new last name. Defaults to None.
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
        self.updated_at = datetime.now()
        data_manager.save(self) # Save the updated user to the data manager


    def host_place(self, place):
        """
        Host a place.

        Args:
            place (Place): The place to be hosted.
        """
        if place.host is not None:
            raise ValueError("Place is already hosted by a user")
        self.places.append(place)
        place.host = self
        data_manager.save(self) # Save the user to the data manager
        data_manager.save(place) # Save the place to the data manager


    def write_review(self, review):
        """
        Write a review.

        Args:
            review (Review): The review to be written.
        """
        self.reviews.append(review) # Add the review to the user's reviews
        data_manager.save(self) # Save the user to the data manager
        data_manager.save(review) # Save the review to the data manager


    @classmethod
    def load(cls, obj_id): 
        """
        Load a user by ID.

        Args:
            obj_id (uuid.UUID): The ID of the user to be loaded.

        Returns:
            User: The loaded user.
        """
        return data_manager.load(cls, obj_id) # Load the user from the data manager


    @classmethod
    def load_all(cls):
        """
        Load all users.

        Returns:
            list: A list of all users.
        """
        return data_manager.load_all(cls) # Load all users from the data manager


    @classmethod
    def delete(cls, obj_id):
        """
        Delete a user by ID.

        Args:
            obj_id (uuid.UUID): The ID of the user to be deleted.
        """
        user = data_manager.load(cls, obj_id) # Load the user
        if user: # Check if the user exists
            del User.users[user.email] # Remove the user from the dictionary
            data_manager.delete(user) # Delete the user from the data manager
