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
    def __init__(self, name, country_code):
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
        self.country_code = country_code
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

    @classmethod
    def from_dict(cls, data):
        """
        Create a City instance from a dictionary.

        Args:
            data (dict): The dictionary containing city data.

        Returns:
            City: The created city instance.
        """
        try:
            city = cls(data['name'], data['country'])
            city.id = uuid.UUID(data['id'])
            city.created_at = datetime.fromisoformat(data['created_at'])
            city.updated_at = datetime.fromisoformat(data['updated_at'])
        except KeyError as e:
            raise ValueError(f"Missing key in data dictionary: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid value in data dictionary: {e}")
        return city
    
    def to_dict(self):
        """
        Convert the City instance to a dictionary.

        Returns:
            dict: The dictionary containing city data.
        """
        return {
            'id': str(self.id), # Convert the 'id' to a string
            'name': self.name, # Use the 'name' attribute
            'country': self.country_code, # Use the 'country' attribute
            'created_at': self.created_at.isoformat(), # Convert 'created_at' to an ISO 8601 string
            'update_at': self.updated_at.isoformat()  # Convert 'updated_at' to an ISO 8601 string
        }
