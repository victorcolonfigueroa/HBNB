import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class BaseModel:
    """
    Represents a base model with an ID, created_at timestamp, and updated_at timestamp.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the BaseModel with an ID, created_at timestamp, and updated_at timestamp.

        :param args: Optional positional arguments
        :param kwargs: Optional keyword arguments
        """
        self.id = uuid.uuid4() if 'id' not in kwargs else uuid.UUID(kwargs['id'])
        self.created_at = datetime.now() if 'created_at' not in kwargs else datetime.fromisoformat(kwargs['created_at'])
        self.updated_at = datetime.now() if 'updated_at' not in kwargs else datetime.fromisoformat(kwargs['updated_at'])
        data_manager.save(self)

    def save(self):
        """
        Save the BaseModel. This updates the updated_at timestamp and saves the BaseModel using the data manager.
        """
        self.updated_at = datetime.now()
        data_manager.save(self)

    @classmethod
    def load(cls, obj_id):
        """
        Load a BaseModel with a given ID.

        :param obj_id: The ID of the BaseModel to load
        :return: The loaded BaseModel
        """
        return data_manager.load(cls, obj_id)

    @classmethod
    def load_all(cls):
        """
        Load all BaseModels of this type.

        :return: A list of all loaded BaseModels of this type
        """
        return data_manager.load_all(cls)

    @classmethod
    def delete(cls, obj_id):
        """
        Delete a BaseModel with a given ID.

        :param obj_id: The ID of the BaseModel to delete
        """
        obj = cls.load(obj_id)
        if obj:
            data_manager.delete(obj)

    def to_dict(self):
        """
        Convert the BaseModel to a dictionary.

        :return: The BaseModel as a dictionary
        """
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a BaseModel from a dictionary.

        :param data: The dictionary to create the BaseModel from
        :return: The created BaseModel
        """
        return cls(**data)
