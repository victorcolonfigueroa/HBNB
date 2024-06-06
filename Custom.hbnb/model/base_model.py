import uuid
import datetime

class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
