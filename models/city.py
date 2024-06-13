from models.base_model import BaseModel
from models.place import Place

class City(BaseModel):
    """
    Represents a city with a name, country code, and list of places.
    """

    def __init__(self, name, country_code, *args, **kwargs):
        """
        Initialize the City with a name and country code.

        :param name: The name of the city
        :param country_code: The country code of the city
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.country_code = country_code
        self.places = []
        self.save()

    def add_place(self, place):
        """
        Add a place to the city.

        :param place: The place to add, either as a Place object or a string ID
        """
        if isinstance(place, str):
            place = Place.load(place)
        if place and place not in self.places:
            self.places.append(place)
            self.save()
            place.save()

    def to_dict(self):
        """
        Convert the City to a dictionary.

        :return: The City as a dictionary
        """
        data = super().to_dict()
        data.update({
            'name': self.name,
            "country_code": self.country_code,
            'places': [place.to_dict() for place in self.places if isinstance(place, Place)]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create a City from a dictionary.

        :param data: The dictionary to create the City from
        :return: The created City
        """
        city = cls(
            name=data['name'],
            country_code=data['country_code'],
            id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        city.places = [Place.from_dict(place) if isinstance(place, dict) else place for place in data.get('places', [])]
        return city
