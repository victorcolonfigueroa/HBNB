import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class City:
    """
    City class represents a city in the system.
    """
    def __init__(self, name, country):
        """
        Initialize a new City instance.

        Args:
            name (str): The name of the city.
            country (str): The country where the city is located.
        """
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.country = country
        self.places = []  # List of places in the city
        self.users = []  # List of users in the city
        data_manager.save(self) # Save the city to the data manager

    def add_place(self, place):
        """
        Add a place to the city.

        Args:
            place (Place): The place to be added.
        """
        self.places.append(place) # Add the place to the list of places
        place.city = self # Set the city of the place to this city
        data_manager.save(self) # Save the city to the data manager
        data_manager.save(place) # Save the place to the data manager

    @classmethod
    def load(cls, obj_id):
        """
        Load a city by ID.

        Args:
            obj_id (uuid.UUID): The ID of the city to be loaded.

        Returns:
            City: The loaded city.
        """
        return data_manager.load(cls, obj_id) # Load the city with the given id
    
    @classmethod
    def load_all(cls):
        """
        Load all cities.

        Returns:
            list: A list of all cities.
        """
        return data_manager.load_all(cls) # Load all cities
    
    @classmethod
    def delete(cls, obj_id):
        """
        Delete a city by ID.

        Args:
            obj_id (uuid.UUID): The ID of the city to be deleted.
        """
        city = data_manager.load(cls, obj_id) # Load the city with the given id
        if city:
            data_manager.delete(city) # Delete the city from the data manager
