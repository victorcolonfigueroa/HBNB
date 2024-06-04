import uuid
from datetime import datetime


class Amenity:
    def __init__(self, name, description):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name
        self.description = description


    # Method to update the amenity details
    def update_amenity(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description
        self.updated_at = datetime.now()
