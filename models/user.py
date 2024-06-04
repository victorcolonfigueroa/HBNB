import uuid
from datetime import datetime


class User:
    users = {} # Dictionary to store all users

    def __init__(self, email, password, first_name, last_name):
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
        User.users[email] = self


    # Method to update the user profile
    def update_profile(self, email=None, password=None, first_name=None, last_name=None):
        if email and email != self.email and email in User.users:
            raise ValueError("User with email {} already exists".format(email))  # Check if the new email is already in use
        if email:
            del User.users[self.email] # Remove the user from the dictionary
            self.email = email  # Update the email
            User.users[self.email] = self  # Add the user back to the dictionary
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.updated_at = datetime.now()


    # Method to host a place
    def host_place(self, place):
        if place.host is not None:
            raise ValueError("Place is already hosted by a user")
        self.places.append(place)
        place.host = self


    # Method to write a review
    def write_review(self, review):
        self.reviews.append(review)
