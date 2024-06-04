import uuid
from datetime import datetime


class Place:
    def __init__(self, name, description, address, city, latitude, longitude,
                 number_of_rooms, bathrooms, price_per_night, max_guests):
        
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.host = None
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = []  # List of amenities available in the place
        self.reviews = []


    # Method to update the place details
    def update_details(self, name=None, description=None, address=None, number_of_rooms=None,
                       bathrooms=None, price_per_night=None, max_guests=None):
        
        if name:
            self.name = name
        if description:
            self.description = description
        if address:
            self.address = address
        if number_of_rooms:
            self.number_of_rooms = number_of_rooms
        if bathrooms:
            self.bathrooms = bathrooms
        if price_per_night:
            self.price_per_night = price_per_night
        if max_guests:
            self.max_guests = max_guests
        self.updated_at = datetime.now()


    # Method to add an amenity
    def add_amenity(self, amenity):
        self.amenities.append(amenity)


    # Method to write a review
    def add_review(self, review):
        self.reviews.append(review)
