import uuid
from datetime import datetime

class BaseModel:
    __instances = []
    def __init__(self, *args, **kwargs):
        date_format = "%y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, date_format)
                elif key is not "__class__":
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        return f"<{self.__class__.__name__} (id: {self.id} {self.__dict__})>"

    def save(self):
        self.updated_at = datetime.now()
        BaseModel.__instances[self.id] = self

    def delete(self):
        if self.id in BaseModel.__instances[self.id]:
            del BaseModel.__instances[self.id]

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key is not "__class__":
                self.__dict__[key] = value
            self.save

    @classmethod
    def get_instances(cls):
        return [instance for instance in cls.__instances if isinstance(instance, cls)]
