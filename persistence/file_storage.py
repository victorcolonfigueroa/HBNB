import json
import os
from datetime import datetime
import uuid
import re
from persistence.ipersistence_manager import IPersistenceManager

class FileStorage(IPersistenceManager):
    """
    FileStorage class that implements the IPersistenceManager interface.
    It uses a JSON file for storing and retrieving data.
    """

    def __init__(self, file_path='/usr/src/app/file_storage.json'):
        """
        Initialize FileStorage with a file path.

        :param file_path: The path to the JSON file used for storage.
        """
        self.file_path = file_path 
        self.data = self._load_file() 

    def _load_file(self):
        """
        Load data from the JSON file.

        :return: A dictionary containing the data loaded from the file.
        """
        if os.path.exists(self.file_path): 
            with open(self.file_path, 'r') as file: 
                return json.load(file) 
        else:
            return {"User": {}, "Place": {}, "Review": {}, "Amenity": {}, "City": {}, "Country": {}}

    def _save_file(self):
        """
        Save the data to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, default=str) 

    def save(self, obj):
        """
        Save an object to the data dictionary and then to the file.

        :param obj: The object to be saved.
        """
        obj_class = obj.__class__.__name__ 
        obj_id = str(obj.id) 
        self.data[obj_class][obj_id] = obj.__dict__ 
        self._save_file() 

    def delete(self, obj):
        """
        Delete an object from the data dictionary and then from the file.

        :param obj: The object to be deleted.
        """
        obj_class = obj.__class__.__name__
        obj_id = str(obj.id)
        if obj_id in self.data[obj_class]: 
            del self.data[obj_class][obj_id] 
            self._save_file()

    def load(self, cls, obj_id):
        """
        Load an object of a given class from the data dictionary using its ID.

        :param cls: The class of the object to be loaded.
        :param obj_id: The ID of the object to be loaded.
        :return: The loaded object if found, None otherwise.
        """
        obj_class = cls.__name__ 
        obj_id = str(obj_id)
        if obj_id in self.data[obj_class]: 
            obj_data = self.data[obj_class][obj_id] 
            obj = cls.__new__(cls) 
            obj.__dict__.update(obj_data) 
            if not isinstance(obj.id, uuid.UUID):
                obj.id = uuid.UUID(obj.id) 

            if isinstance(obj.created_at, str):
                obj.created_at = datetime.fromisoformat(obj.created_at)

            if isinstance(obj.updated_at, str):
                obj.updated_at = datetime.fromisoformat(obj.updated_at)

            return obj 
        return None 

    def load_all(self, cls):
        """
        Load all objects of a given class from the data dictionary.

        :param cls: The class of the objects to be loaded.
        :return: A list of loaded objects.
        """
        obj_class = cls.__name__
        return [self.load(cls, obj_id) for obj_id in self.data[obj_class]]
