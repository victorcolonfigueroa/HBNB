import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from user import User
from Base_model import BaseModel

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Place(BaseModel):
    """
    Place class represents a place in the system.
    """
    def __init__(self, name, description, address, city, latitude, longitude,
                 number_of_rooms, bathrooms, price_per_night, max_guests):
        """
        Initialize a new Place instance.

        Args:
            name (str): The name of the place.
            description (str): The description of the place.
            address (str): The address of the place.
            city (str): The city where the place is located.
            latitude (float): The latitude of the place.
            longitude (float): The longitude of the place.
            number_of_rooms (int): The number of rooms in the place.
            bathrooms (int): The number of bathrooms in the place.
            price_per_night (float): The price per night for the place.
            max_guests (int): The maximum number of guests the place can accommodate.
        """
        super().__init__()
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
        self.reviews = [] # List of reviews for the place
        data_manager.save(self) # Save the place to the data manager
        
    def assing_id(self):
        id = User.self.id
        host_id = super().host(self, id)
        self.host = host_id

    def update_details(self, name=None, description=None, address=None, number_of_rooms=None,
                       bathrooms=None, price_per_night=None, max_guests=None):
        """
        Update the place's details.

        Args:
            name (str, optional): The new name. Defaults to None.
            description (str, optional): The new description. Defaults to None.
            address (str, optional): The new address. Defaults to None.
            number_of_rooms (int, optional): The new number of rooms. Defaults to None.
            bathrooms (int, optional): The new number of bathrooms. Defaults to None.
            price_per_night (float, optional): The new price per night. Defaults to None.
            max_guests (int, optional): The new maximum number of guests. Defaults to None.
        """
        if name:
            self.name = name # Update the name
        if description:
            self.description = description # Update the description
        if address:
            self.address = address # Update the address
        if number_of_rooms:
            self.number_of_rooms = number_of_rooms # Update the number of rooms
        if bathrooms:
            self.bathrooms = bathrooms # Update the number of bathrooms
        if price_per_night:
            self.price_per_night = price_per_night # Update the price per night
        if max_guests:
            self.max_guests = max_guests # Update the maximum number of guests
        self.updated_at = datetime.now() # Update the updated_at timestamp
        data_manager.save(self) # Save the updated place details

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        Args:
            amenity (Amenity): The amenity to be added.
        """
        self.amenities.append(amenity) # Add the amenity to the list
        data_manager.save(self) # Save the updated place details

    def add_review(self, review):
        """
        Add a review to the place.

        Args:
            review (Review): The review to be added.
        """
        self.reviews.append(review) # Add the review to the list
        data_manager.save(self) # Save the updated place details
        data_manager.save(review) # Save the review to the data manager

    @classmethod
    def load(cls, obj_id):
        """
        Load a place by ID.

        Args:
            obj_id (uuid.UUID): The ID of the place to be loaded.

        Returns:
            Place: The loaded place.
        """
        return data_manager.load(cls, obj_id) # Load the place with the given id

    @classmethod
    def load_all(cls):
        """
        Load all places.

        Returns:
            list: A list of all places.
        """
        return data_manager.load_all(cls) # Load all places from the data manager

    @classmethod
    def delete(cls, obj_id):
        """
        Delete a place by ID.

        Args:
            obj_id (uuid.UUID): The ID of the place to be deleted.
        """
        place = data_manager.load(cls, obj_id) # Load the place with the given id
        if place: # Check if the place exists
            data_manager.delete(place) # Delete the place from the data manager
