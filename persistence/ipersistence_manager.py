from abc import ABC, abstractmethod


class IPersistenceManager(ABC):
    @abstractmethod
    def save(self, obj):
        pass

    @abstractmethod
    def delete(self, obj):
        pass

    @abstractmethod
    def load(self, obj):
        pass

    @abstractmethod
    def load_all(self, obj):
        pass
