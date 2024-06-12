from persistance_manager import IPersistenceManager

'''
entity=objeto
cls = clase
entity type = review place amenity area code los detalles del objeto
'''
class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {}

    def save(self, object):
        self.storage[object.id] = object

    def get(self, object_id, object_type):
        return self.storage.get(object_id, None)

    def update(self, entity):
        if entity.id in self.storage:
            self.storage[entity.id] = entity

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage:
            del self.storage[entity_id]

    def load(self, cls, entity_id):
        return self.storage.load(cls, entity_id)

    def load_all(self, cls):
        return self.storage.load_all(cls)
