import uuid
from datetime import datetime


class User:
    def __init__(self, email, password, first_name, last_name):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = [] # List of places hosted by the user
        self.reviews = [] # List of reviews made by the user


    # Method to update the user profile
    def update_profile(self, email=None, password=None, first_name=None, last_name=None):
        if email:
            self.email = email
        if password:
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self.updated_at = datetime.now()

