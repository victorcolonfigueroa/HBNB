from persistence.ipersistence_manager import IPersistenceManager

class DataManager(IPersistenceManager):
    """
    DataManager class that implements the IPersistenceManager interface.
    It uses a storage object to perform save, delete, load, and load_all operations.
    """

    def __init__(self, storage):
        """
        Initialize DataManager with a storage object.

        :param storage: The storage object that will be used for persistence operations.
        """
        self.storage = storage

    def save(self, obj):
        """
        Save an object to the storage.

        :param obj: The object to be saved.
        """
        self.storage.save(obj)

    def delete(self, obj):
        """
        Delete an object from the storage.

        :param obj: The object to be deleted.
        """
        self.storage.delete(obj)

    def load(self, cls, obj_id):
        """
        Load an object of a given class from the storage using its ID.

        :param cls: The class of the object to be loaded.
        :param obj_id: The ID of the object to be loaded.
        :return: The loaded object if found, None otherwise.
        """
        return self.storage.load(cls, obj_id)

    def load_all(self, cls):
        """
        Load all objects of a given class from the storage.

        :param cls: The class of the objects to be loaded.
        :return: A list of loaded objects.
        """
        return self.storage.load_all(cls)
