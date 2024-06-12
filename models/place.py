import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from models.review import Review
from models.amenity import Amenity

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Place:
    """
    Place class represents a place in the system.
    """
    places = {}  # Dictionary to store all places

    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, amenity_ids):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids
        self.review = []
        data_manager.save(self)

    def add_review(self, review):
        self.reviews.append(review)
        data_manager.save(self)
        data_manager.save(review)

    def update_details(self, name=None, description=None, address=None, city_id=None, latitude=None, longitude=None, host_id=None, number_of_rooms=None, number_of_bathrooms=None, price_per_night=None, max_guests=None, amenity_ids=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if address:
            self.address = address
        if city_id:
            self.city_id = city_id
        if latitude:
            self.latitude = latitude
        if longitude:
            self.longitude = longitude
        if host_id:
            self.host_id = host_id
        if number_of_rooms:
            self.number_of_rooms = number_of_rooms
        if number_of_bathrooms:
            self.number_of_bathrooms = number_of_bathrooms
        if price_per_night:
            self.price_per_night = price_per_night
        if max_guests:
            self.max_guests = max_guests
        if amenity_ids is not None:
            self.amenity_ids = amenity_ids
        self.updated_at = datetime.now()
        data_manager.save(self)

    @classmethod
    def load(cls, obj_id):
        return data_manager.load(cls, obj_id)

    @classmethod
    def load_all(cls):
        return data_manager.load_all(cls)

    @classmethod
    def delete(cls, obj_id):
        place = data_manager.load(cls, obj_id)
        if place:
            data_manager.delete(place)

    @classmethod
    def from_dict(cls, data):
        place = cls(
            name=data['name'],
            description=data['description'],
            address=data['address'],
            city_id=data['city_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            host_id=data['host_id'],
            number_of_rooms=data['number_of_rooms'],
            number_of_bathrooms=data['number_of_bathrooms'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            amenity_ids=data['amenity_ids']
        )
        place.id = uuid.UUID(data['id'])
        place.created_at = datetime.fromisoformat(data['created_at'])
        place.updated_at = datetime.fromisoformat(data['updated_at'])
        place.reviews = [Review.from_dict(review) for review in data.get('reviews', [])]
        return place

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': str(self.city_id) if self.city_id else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': str(self.host_id) if self.host_id else None,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenity_ids': [str(amenity_id) for amenity_id in self.amenity_ids] if self.amenity_ids else None,
            'reviews': [review.to_dict() for review in self.reviews],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
