from persistence.ipersistence_manager import IPersistenceManager


class DataManager(IPersistenceManager):
    def __init__(self, storage):
        self.storage = storage

    def save(self, obj):
        self.storage.save(obj)

    def delete(self, obj):
        self.storage.delete(obj)

    def load(self, cls, obj_id):
        return self.storage.load(cls, obj_id)

    def load_all(self, cls):
        return self.storage.load_all(cls)
