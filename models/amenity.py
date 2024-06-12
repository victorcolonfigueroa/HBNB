import uuid
from datetime import datetime
from persistence.data_manager import DataManager
from persistence.file_storage import FileStorage
from models.Base_model import BaseModel

# Create an instance of DataManager
storage = FileStorage()
data_manager = DataManager(storage)

class Amenity(BaseModel):
    """
    Amenity class represents an amenity in the system.
    """
    def __init__(self, name, description):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): The name of the amenity.
            description (str): The description of the amenity.
        """
        super().__init__()
        self.name = name
        self.description = description
        data_manager.save(self) # Save the amenity to the data manager

    def update_amenity(self, name=None, description=None):
        """
        Update the amenity's details.

        Args:
            name (str, optional): The new name. Defaults to None.
            description (str, optional): The new description. Defaults to None.
        """
        if name:
            self.name = name # Update the name
        if description:
            self.description = description # Update the description
        self.updated_at = datetime.now() # Update the updated_at timestamp
        data_manager.save(self) # Save the updated amenity to the data manager

    @classmethod
    def load(cls, obj_id):
        """
        Load an amenity by ID.

        Args:
            obj_id (uuid.UUID): The ID of the amenity to be loaded.

        Returns:
            Amenity: The loaded amenity.
        """
        return data_manager.load(cls, obj_id) # Load the amenity with the given id

    @classmethod
    def load_all(cls):
        """
        Load all amenities.

        Returns:
            list: A list of all amenities.
        """
        return data_manager.load_all(cls) # Load all amenities from the data manager

    @classmethod
    def delete(cls, obj_id):
        """
        Delete an amenity by ID.

        Args:
            obj_id (uuid.UUID): The ID of the amenity to be deleted.
        """
        amenity = data_manager.load(cls, obj_id) # Load the amenity with the given id
        if amenity: # Check if the amenity exists
            data_manager.delete(amenity) # Delete the amenity from the data manager
