from Address import Address
from ModHash import ModHash

class Location:
    def __init__(self, fullAddress = "", distance = -1, size = 33):
        
        self.address = Address(fullAddress = fullAddress)
        self.id = self.address.address
        self.distance = distance
        self.targetLocations = ModHash(size)

    def add_target(self, location):
        self.targetLocations.add(location)

    def __eq__(self, address: object) -> bool:
        return self.address == address
    
    def __str__(self) -> str:
        return self.address.address