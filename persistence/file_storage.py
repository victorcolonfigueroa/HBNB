import json
import os
from datetime import datetime
import uuid
from persistence.ipersistence_manager import IPersistenceManager


class FileStorage(IPersistenceManager):
    def __init__(self, file_path='file_storage.json'):
        self.file_path = file_path 
        self.data = self._load_file() 

    def _load_file(self):
        if os.path.exists(self.file_path): # Check if the file exists
            with open(self.file_path, 'r') as file: # Open the file
                return json.load(file) # Load the data from the file
    
        else:
            return {"User": {}, "Place": {}, "Review": {}, "Amenity": {}, "City": {}, "Country": {}} # Dictionary to store all data


    def _save_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, default=str) 


    def save(self, obj):
        obj_class = obj.__class__.__name__ # Get the class name of the object
        obj_id = str(obj.id) # Get the id of the object
        self.data[obj_class][obj_id] = obj.__dict__ # Save the object in the data dictionary
        self._save_file() # Save the data to the file


    def delete(self, obj):
        obj_class = obj.__class__.__name__
        obj_id = str(obj.id)
        if obj_id in self.data[obj_class]: # Check if the object exists
            del self.data[obj_class][obj_id] # Delete the object from the data dictionary
            self._save_file()


    def load(self, cls, obj_id):
        obj_class = cls.__name__ # Get the class name
        obj_id = str(obj_id)
        if obj_id in self.data[obj_class]: # Check if the object exists
            obj_data = self.data[obj_class][obj_id] # Get the object data
            obj = cls.__new__(cls) # Create a new object of the class
            obj.__dict__.update(obj_data) # Update the object with the data
            if not isinstance(obj.id, uuid.UUID):
                obj.id = uuid.UUID(obj.id) # Convert the id to UUID

            if isinstance(obj.created_at, str):
                obj.created_at = datetime.fromisoformat(obj.created_at)  # Convert the created_at to datetime only if it's a string

            if isinstance(obj.updated_at, str):
                obj.updated_at = datetime.fromisoformat(obj.updated_at)  # Convert the updated_at to datetime only if it's a string

            return obj 
        return None # Return None if the object does not exist


    def load_all(self, cls):
        obj_class = cls.__name__
        return [self.load(cls, obj_id) for obj_id in self.data[obj_class]] # Load all objects of the class
