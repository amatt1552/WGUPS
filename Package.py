from Address import Address
from datetime import datetime, time
from Enums import PackageStatus
class Package:
    
    class DeliveryStatus():
        def __init__(self, packageStatus = PackageStatus.ATHUB, deliveryTime = "Not Delivered", onTime = False):
            self.packageStatus = packageStatus
            self.deliveryTime = deliveryTime
            self.onTime = onTime
        
        def __str__(self) -> str:
            
            deliverTimeMessage = self.deliveryTime
            if(type(deliverTimeMessage) != str):
                deliverTimeMessage = deliverTimeMessage.strftime("%I:%M %p")
            
            return self.packageStatus.get_name()  + ", " + self.on_time_to_str() + " | Delivery Time: " + deliverTimeMessage

        def on_time_to_str(self):
            onTimeMessage = "Late"
            if(self.onTime):
                onTimeMessage = "On Time"
            return onTimeMessage

        def __eq__(self, value) -> bool:
            if(type(value) == self):
                return self.packageStatus == value.packageStatus and self.deliveryTime == value.deliveryTime and self.onTime == value.onTime
            return False


    def __init__(self, id = -1, address = "", city = "", state = "", zip = "", deadline = "EOD", weight = -1, notes = ""):
        self.id = id
        self.address = Address("", address, city, state, zip)
        self.oldAddress = Address("", address, city, state, zip)
        
        if(type(deadline) == str):
            if(deadline == "EOD"):
                deadline = "11:59 PM"
            self.deadline = datetime.strptime(deadline,"%I:%M %p").time()
        else:
            self.deadline = deadline

        self.weight = weight
        self.notes = notes
        
        self.deliveryStatus = self.DeliveryStatus(PackageStatus.ATHUB)

    def set_delivered(self, deliveredTime):
        if(type(deliveredTime) == str):
            deliveredTime = datetime.strptime(deliveredTime,"%I:%M %p").time()
        self.deliveryStatus = self.DeliveryStatus(PackageStatus.DELIVERED, deliveredTime, deliveredTime <= self.deadline)

    def on_time_check(self, deliveredTime):
        self.deliveryStatus.onTime = deliveredTime <= self.deadline

    def set_enroute(self):
        self.deliveryStatus = self.DeliveryStatus(PackageStatus.ENROUTE)

    def set_at_hub(self):
        self.deliveryStatus = self.DeliveryStatus(PackageStatus.ATHUB)
    
    def change_address(self, address):
        if(self.deliveryStatus.packageStatus == PackageStatus.DELIVERED):
            self.deliveryStatus.onTime = False
        #print("address changed for package", self.id)
        self.deliveryStatus.packageStatus = PackageStatus.WRONG_ADDRESS
        self.address.change_address(fullAddress=address)
    
    def __str__(self) -> str:
        returnedValue = "Package ID: "
        returnedValue += str(self.id) 
        returnedValue += " | Package Weight: "
        returnedValue += str(self.weight)
        returnedValue += " | Full Address: " 
        returnedValue += str(self.address)
        #returnedValue += " | Old Address: " 
        #returnedValue += str(self.oldAddress)
        returnedValue += " | Delivery Status: "
        returnedValue += str(self.deliveryStatus)
        returnedValue += " | Deadline: "
        returnedValue += self.deadline.strftime("%I:%M %p")
        
        return returnedValue
    
    #helps with sorting.
    def __lt__(self, value) -> bool:
        if(type(value) == Package):
            return value.id < self.id
        elif(type(value) == int):
            return value < self.id
        return False

    #helps lookup packages. check eq in address to see how addresses are handled.
    def __eq__(self, value) -> bool:
        if(type(value) == Package):
            if(value.id == self.id):
                return True

        elif(type(value) == int):
            if(value == self.id):
                return True
            elif(value == self.weight):
                return True
            #for zipcode
            elif(str(value) == self.address):
                return True

        elif(type(value) == str):
            try:
                if(int(value) == self.id):
                    return True
            except:
                pass
            try:
                if(int(value) == self.weight):
                    return True
            except:
                pass
            if(value == self.address):
                return True
            elif(value == self.address.city):
                return True
            elif(value == self.address.state):
                return True
            try:
                if(datetime.strptime(value,"%I:%M %p").time() == self.deadline):
                    return True
            except:
                if(value == self.deadline):
                    return True
            try:
                if(datetime.strptime(value,"%I:%M %p").time() == self.deliveryStatus.deliveryTime):
                    return True
            except:
                if(value == self.deliveryStatus.deliveryTime):
                    return True
            if(value == self.deliveryStatus.on_time_to_str()):
                return True
            elif(value == self.deliveryStatus.packageStatus.get_name()):
                return True

        elif(type(value) == self.DeliveryStatus):
            if(value == self.deliveryStatus):
                return True

        elif(type(value) == PackageStatus):
            if(value == self.deliveryStatus.packageStatus):
                return True

        elif(type(value) != str):
            if(value == self.deliveryStatus.deliveryTime):
                return True
            elif(value == self.deadline):
                return True
        return False
