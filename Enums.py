from enum import Enum
class PackageStatus(Enum):
    ATHUB = 1
    ENROUTE = 2
    DELIVERED = 3
    WRONG_ADDRESS = 4
    
    def get_name(self):
            if(self.value == 1):
                return "At Hub"
            if(self.value == 2):
                return "Enroute"
            if(self.value == 3):
                return "Delivered"
            if(self.value == 4):
                return "Wrong Address"