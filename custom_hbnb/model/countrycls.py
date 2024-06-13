from model.base_model import BaseModel
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from model.placescls import Place
import pycountry #type: ignore
from datetime import datetime
import uuid


# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Country(BaseModel):
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
        super().__init__()
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

class City(BaseModel):
    """
    City class represents a city in the system.
    """
    cities = {} # Dictionary to store all cities

    def __init__(self, name, country_id):
        """
        Initialize a new City instance.

        Args:
            name (str): The name of the city.
            country (str): The country where the city is located.
        """
        super().__init__()
        self.name = name
        self.country_id = country_id
        self.places = []  # List of places in the city
        DataManager.save(self) # Save the city to the data manager

    def add_place(self, place):
        """
        Add a place to the city.

        Args:
            place (Place): The place to be added.
        """
        self.places.append(place) # Add the place to the list of places
        DataManager.save(self) # Save the city to the data manager
        DataManager.save(place) # Save the place to the data manager

    def update_details(self, name=None, country_id=None):
        if name:
            self.name = name # Update the 'name' attribute
        if country_id:
            self.country_id = country_id # Update the 'country_id' attribute
        self.updated_at = datetime.now() # Update the 'updated_at' attribute
        DataManager.save(self) # Save the city to the data manager

    @staticmethod
    def load(obj_id):
        """
        Load a city by ID.

        Args:
            obj_id (uuid.UUID): The ID of the city to be loaded.

        Returns:
            City: The loaded city.
        """
        return DataManager.load(City, obj_id) # Load the city with the given id

    @classmethod
    def load_all(cls):
        """
        Load all cities.

        Returns:
            list: A list of all cities.
        """
        return DataManager.load_all(cls) # Load all cities

    @classmethod
    def delete(cls, obj_id):
        """
        Delete a city by ID.

        Args:
            obj_id (uuid.UUID): The ID of the city to be deleted.
        """
        city = DataManager.load(cls, obj_id) # Load the city with the given id
        if city:
            DataManager.delete(city) # Delete the city from the data manager

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
            city = cls(data['name'], data['country_id'])
            city.id = uuid.UUID(data['id'])
            city.created_at = datetime.fromisoformat(data['created_at'])
            city.updated_at = datetime.fromisoformat(data['updated_at'])
            city.places = [Place.from_dict(place) for place in data.get('places', [])]
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
            'country_id': str(self.country_id) if self.country_id else None, # Convert 'country_id' to a string if it exists
            'created_at': self.created_at.isoformat(), # Convert 'created_at' to an ISO 8601 string
            'updated_at': self.updated_at.isoformat(),  # Convert 'updated_at' to an ISO 8601 string
            'places': [place.to_dict() for place in self.places] # Serialize the list of places
        }
