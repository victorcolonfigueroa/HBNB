import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.update_at = datetime.now()
        
    def save(self):
        self.update_at = datetime.now()
        
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'update_at': self.update_at.isoformat()
        }
        
def host(self, id):
    id = self.id 
    return id
