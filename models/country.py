from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
import uuid
from datetime import datetime

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Country:
    """
    Country class represents a country in the system.
    """
    def __init__(self, name):
        """
        Initialize a new Country instance.

        Args:
            name (str): The name of the country.
        """
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.cities = [] # List of cities in the country
        data_manager.save(self) # Save the country to the data manager

    def add_city(self, city):
        """
        Add a city to the country.

        Args:
            city (City): The city to be added.
        """
        self.cities.append(city) # Add the city to the list of cities
        data_manager.save(self) # Save the country to the data manager
        data_manager.save(city) # Save the city to the data manager

    @classmethod
    def load(cls, obj_id):
        """
        Load a country by ID.

        Args:
            obj_id (uuid.UUID): The ID of the country to be loaded.

        Returns:
            Country: The loaded country.
        """
        return data_manager.load(cls, obj_id) # Load the country with the given id
    
    @classmethod
    def load_all(cls):
        """
        Load all countries.

        Returns:
            list: A list of all countries.
        """
        return data_manager.load_all(cls) # Load all countries
    
    @classmethod
    def delete(cls, obj_id):
        """
        Delete a country by ID.

        Args:
            obj_id (uuid.UUID): The ID of the country to be deleted.
        """
        country = data_manager.load(cls, obj_id) # Load the country with the given id
        if country:
            data_manager.delete(country) # Delete the country from the data manager
