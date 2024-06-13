from models.base_model import BaseModel
from models.review import Review
from models.amenity import Amenity

class Place(BaseModel):
    """
    Represents a place with various attributes such as name, description, address, etc.
    """
    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, amenity_ids, *args, **kwargs):
        """
        Initialize the Place with various attributes.

        :param name: The name of the place
        :param description: The description of the place
        :param address: The address of the place
        :param city_id: The ID of the city the place is in
        :param latitude: The latitude of the place
        :param longitude: The longitude of the place
        :param host_id: The ID of the host of the place
        :param number_of_rooms: The number of rooms in the place
        :param number_of_bathrooms: The number of bathrooms in the place
        :param price_per_night: The price per night to stay at the place
        :param max_guests: The maximum number of guests the place can accommodate
        :param amenity_ids: The IDs of the amenities the place has
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
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
        self.reviews = [] # List of Review instances
        self.amenities = [] # List of Amenity instances
        self.host = None
        self.save()

    def add_review(self, review):
        """
        Add a review to the place.

        :param review: The review to add
        """
        if isinstance(review, str):
            review = Review.load(review)
        if review and review not in self.reviews:
            if review.review_author == self.host:
                raise ValueError("A host cannot review their own listing")
            self.reviews.append(review)
            self.save()
            review.save()

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        :param amenity: The amenity to add
        """
        if isinstance(amenity, str):
            amenity = Amenity.load(amenity)
        if amenity and amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()
            amenity.add_place(self)

    def update_details(self, name=None, description=None, address=None, city_id=None, latitude=None, longitude=None, host_id=None, number_of_rooms=None, number_of_bathrooms=None, price_per_night=None, max_guests=None, amenity_ids=None):
        """
        Update the details of the place.

        :param name: The new name of the place
        :param description: The new description of the place
        :param address: The new address of the place
        :param city_id: The new ID of the city the place is in
        :param latitude: The new latitude of the place
        :param longitude: The new longitude of the place
        :param host_id: The new ID of the host of the place
        :param number_of_rooms: The new number of rooms in the place
        :param number_of_bathrooms: The new number of bathrooms in the place
        :param price_per_night: The new price per night to stay at the place
        :param max_guests: The new maximum number of guests the place can accommodate
        :param amenity_ids: The new IDs of the amenities the place has
        """
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
        if host_id and self.host_id != host_id:
            raise ValueError("Listing already has a host")
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
        self.save()

    def to_dict(self):
        """
        Convert the Place to a dictionary.

        :return: The Place as a dictionary
        """
        data = super().to_dict()
        data.update({
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
            'reviews': [review.to_dict() for review in self.reviews if isinstance(review, Review)],
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create a Place from a dictionary.

        :param data: The dictionary to create the Place from
        :return: The created Place
        """
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
            amenity_ids=data['amenity_ids'],
            id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        place.reviews = [Review.from_dict(review) if isinstance(review, dict) else review for review in data.get('reviews', [])]
        place.amenities = [Amenity.from_dict(amenity) if isinstance(amenity, dict) else amenity for amenity in data.get('amenities', [])]
        return place
