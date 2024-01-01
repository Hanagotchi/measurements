from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def insert_into_device_plant(self, id_device, id_plant, plant_type, id_user):
        pass

    @abstractmethod
    def find_in_device_plant(self, id_device):
        pass

    @abstractmethod
    def clean_device_plant(self):
        pass