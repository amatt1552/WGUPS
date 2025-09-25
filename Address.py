
class Address:
    def __init__(self, name = "", address = "", city = "", state = "", zip = "", fullAddress = "") -> None:
        #tries to set the address if given a full address.
        if(fullAddress != ""):
            name = ""
            address = ""
            city = ""
            state = ""
            zip = ""
            splitAddress = fullAddress.split(", ")
            try:
                if(len(splitAddress) > 4):
                    name = splitAddress[0]
                    address = splitAddress[1]
                    city = splitAddress[2]
                    state = splitAddress[3]
                    zip = splitAddress[4]
                else:
                    name = splitAddress[0]
                    address = splitAddress[1]
                    zip = splitAddress[2]
            except(IndexError):
                pass
                print("Something was not set in the address! Make sure its correct.", "\n\tname: " + name, "\n\taddress: " + address, "\n\tcity: " + city, "\n\tstate: " + state, "\n\tzipcode: " + zip,)
        else:
            if(name != ""):
                fullAddress = name + ", "
            if(address != ""):
               fullAddress += address + ", "
            if(city != ""):
                fullAddress += city + ", " 
            if(state != ""):
                fullAddress += state + ", "
            if(zip != ""):
                fullAddress += zip
        
        self.fullAddress = fullAddress
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
    
    def change_address(self, newName = "udef", newAddress = "udef", newCity = "udef", newState = "udef", newZip = "udef", fullAddress = "udef") -> None:
        if(fullAddress != "udef"):
            newName = ""
            newAddress = ""
            newCity = ""
            newState = ""
            newZip = ""
            splitAddress = fullAddress.split(", ")
            try:
                if(len(splitAddress) > 4):
                    newName = splitAddress[0]
                    newAddress = splitAddress[1]
                    newCity = splitAddress[2]
                    newState = splitAddress[3]
                    newZip = splitAddress[4]
                else:
                    newName = splitAddress[0]
                    newAddress = splitAddress[1]
                    newZip = splitAddress[2]
            except(IndexError):
                pass
                print("Something was not set in change_address! Make sure its correct.", "\n\tname: " + newName, "\n\taddress: " + newAddress, "\n\tcity: " + newCity, "\n\tstate: " + newState, "\n\tzipcode: " + newZip,)
        else:
            if(newName != "udef"):
                fullAddress = newName + ", "
            if(newAddress != "udef"):
               fullAddress += newAddress + ", "
            if(newCity != "udef"):
                fullAddress += newCity + ", " 
            if(newState != "udef"):
                fullAddress += newState + ", "
            if(newZip != "udef"):
                fullAddress += newZip
        
        if(fullAddress != "udef"):
            self.fullAddress = fullAddress            
        if(newName != "udef"):
            self.name = newName        
        if(newAddress != "udef"):
            self.address = newAddress
        if(newCity != "udef"):
            self.city = newCity
        if(newState != "udef"):
            self.state = newState
        if(newZip != "udef"):
            self.zip = newZip

    def __str__(self) -> str:
        return self.fullAddress

    def __lt__(self, address) -> bool:
        if(type(address) == Address):
            return self.address.address < address.address
        if(type(address) == str):
            return self.address.address < address

    def __gt__(self, address) -> bool:
        return self.address.address > address.address  

    def __eq__(self, address) -> bool:
        #print(address + " ==", self.address + "?")
        if(type(address) == Address):
            if(address.fullAddress == self.fullAddress):
                return True
            if(address.address == self.address):
                return True
            if(address.zip == self.zip):
                return True
        elif(type(address) == str):
            if(address == self.fullAddress):
                return True
            if(address == self.address):
                return True
            if(address == self.zip):
                return True
        return False