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
    countries = {} # Dictionary to store all countries

    def __init__(self, name, code, cities=None):
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
        Country.countries[self.id] = self # Add the country to the dictionary
        self.cities = cities if cities is not None else [] # List of cities in the country
        data_manager.save(self) # Save the country to the data manager

    

    def add_city(self, city):
        """
        Add a city to the country.

        Args:
            city (City): The city to be added.
        """
        self.cities.append(city.id) # Add the city to the list of cities
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
        try:
            country = cls(data['name'], data['code'])
            country.id = uuid.UUID(data['id'])
            country.created_at = datetime.fromisoformat(data['created_at'])
            country.updated_at = datetime.fromisoformat(data['updated_at'])

            from models.city import City
            country.cities = [City.from_dict(city) for city in data.get('cities', [])]  # Deserialize cities

        except KeyError as e:
            raise ValueError(f"Missing key in data dictionary: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid value in data dictionary: {e}")
        return country
    
    def to_dict(self):
        """
        Convert the Country instance to a dictionary.

        Returns:
            dict: The dictionary containing country data.
        """
        from models.city import City

        return {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            # Serialize cities
            'cities': [city.to_dict() for city in (data_manager.load(City, city_id) for city_id in self.cities) if city is not None]
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
