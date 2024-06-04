import uuid
from datetime import datetime


class City:
    def __init__(self, name, country):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.country = country
        self.places = []  # List of places in the city
        self.users = []  # List of users in the city


    def add_place(self, place):
        self.places.append(place)
        place.city = self
