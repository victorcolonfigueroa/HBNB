from models.base_model import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity with a name and associated places.
    """

    def __init__(self, name, *args, **kwargs):
        """
        Initialize the Amenity with a name and optional arguments.

        :param name: The name of the amenity
        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.places = []
        self.save()

    def add_place(self, place):
        """
        Add a place to the amenity. If the place is not already associated with the amenity, it is added.

        :param place: The place to add, either as a Place object or a string ID
        """
        from models.place import Place

        if isinstance(place, str):
            place = Place.load(place)
        if place and place not in self.places:
            self.places.append(place)
            self.save()
            place.save()

    def to_dict(self):
        """
        Convert the Amenity to a dictionary.

        :return: The Amenity as a dictionary
        """
        data = super().to_dict()
        data.update({
            'name': self.name,
            'places': [place.to_dict() for place in self.places]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Create an Amenity from a dictionary.

        :param data: The dictionary to create the Amenity from
        :return: The created Amenity
        """
        return cls(
            name=data['name'],
            id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
