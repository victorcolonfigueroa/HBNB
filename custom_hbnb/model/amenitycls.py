import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Amenity:
    """
    Amenity class represents an amenity in the system.
    """
    def __init__(self, name, description):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.description = description
        data_manager.save(self)

    def update_amenity(self, name=None):
        if name:
            self.name = name
        self.updated_at = datetime.now()
        data_manager.save(self)

    @classmethod
    def load(cls, obj_id):
        return data_manager.load(cls, obj_id)

    @classmethod
    def load_all(cls):
        return data_manager.load_all(cls)

    @classmethod
    def delete(cls, obj_id):
        amenity = data_manager.load(cls, obj_id)
        if amenity:
            data_manager.delete(amenity)

    @classmethod
    def from_dict(cls, data):
        amenity = cls(data['name'])
        amenity.id = uuid.UUID(data['id'])
        amenity.created_at = datetime.fromisoformat(data['created_at'])
        amenity.updated_at = datetime.fromisoformat(data['updated_at'])
        return amenity

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
