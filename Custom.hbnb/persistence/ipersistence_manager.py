from abc import ABC, abstractmethod

class IPersistenceManager(ABC):
    """
    IPersistenceManager is an abstract base class that defines the interface for a persistence manager.
    It declares methods for saving, deleting, loading a single object, and loading all objects.
    """

    @abstractmethod
    def save(self, obj):
        """
        Save an object. This method should be implemented by subclasses.

        :param obj: The object to be saved.
        """
        pass

    @abstractmethod
    def delete(self, obj):
        """
        Delete an object. This method should be implemented by subclasses.

        :param obj: The object to be deleted.
        """
        pass

    @abstractmethod
    def load(self, obj):
        """
        Load an object. This method should be implemented by subclasses.

        :param obj: The object to be loaded.
        :return: The loaded object if found, None otherwise.
        """
        pass

    @abstractmethod
    def load_all(self, obj):
        """
        Load all objects. This method should be implemented by subclasses.

        :param obj: The class of the objects to be loaded.
        :return: A list of loaded objects.
        """
        pass
