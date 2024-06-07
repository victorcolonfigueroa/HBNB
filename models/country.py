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
    def __init__(self, name, code):
        """
        Initialize a new Country instance.

        Args:
            name (str): The name of the country.
        """
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.code = code
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

    @classmethod
    def from_dict(cls, data):
        """
        Create a Country instance from a dictionary.

        Args:
            data (dict): The dictionary containing country data.

        Returns:
            Country: The created country instance.
        """
        country = cls(data['name'], data['code']) # Create a new instance of the class using the 'name' and 'code' from the data dictionary
        country.id = uuid.UUID(data['id'])  # Set the 'id' of the instance using the 'id' from the data dictionary
        country.created_at = datetime.fromisoformat(data['created_at'])  # Set the 'created_at' of the instance using the 'created_at' from the data dictionary
        country.updated_at = datetime.fromisoformat(data['update_at']) # Set the 'updated_at' of the instance using the 'update_at' from the data dictionary
        return country
    
    def to_dict(self):
        """
        Convert the Country instance to a dictionary.

        Returns:
            dict: The dictionary containing country data.
        """
        return {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat(),
            'update_at': self.updated_at.isoformat()
        }

    @classmethod
    def load_by_code(cls, code):
        """
        Load a country by its code.

        Args:
            code (str): The code of the country to be loaded.

        Returns:
            Country: The loaded country.
        """
        all_countries = cls.load_all()  # Load all instances of the class
        for country in all_countries:  # Iterate over each instance
            if country.code == code: 
                return country  # If a match is found, return the instance
        return None  # If no match is found after checking all instances, return None
