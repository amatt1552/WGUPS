"""
This contains details about the truck and deliveries.
"""
from datetime import datetime, time
import math
from Address import Address
import LocationManager
from Package import Package
import PackageManager
import Events

class Truck:
    
    def __init__(self, id, startTime = "8:00 AM", maxWeight = 2000, maxPackages = 16):
        self.currentWeight = 0
        #will contain the ids of packages
        self.packages = list()
        self.maxWeight = maxWeight
        self.maxPackages = maxPackages
        self.mph = 18
        self.id = id
        self.distanceTraveled = 0.0
        #sets to hub location
        self.startLocation = LocationManager.locations.find("4001 South 700 East")
        self.currentLocation = self.startLocation
        self.returnedTime = None
        self.startTime = startTime
        self.deliveredAll = False
        self.atHub = True

    def add_package(self, packageId):
        package = PackageManager.packages.find(packageId)
        if(package != None):
            if(self.has_space(package)):
                self.packages.append(packageId)
                self.currentWeight += package.weight
            else:
                print("Package does not fit!")

    def add_packages(self, packageIdList):
        """
        Adds list of new packages to packages. Its only useful if you already know the order.
        """
        self.packages.extend(packageIdList)

    def start_delivery(self,targetTime = "11:59 pm", orderFound = False):
        """
        Initializes the delivery process.
        """
        #turn string into a time if string
        if(type(targetTime) == str):
            targetTime = datetime.strptime(targetTime ,"%I:%M %p").time()
        if(type(self.startTime) == str):
            self.startTime = datetime.strptime(self.startTime ,"%I:%M %p").time()
        #print(targetTime, "time")
        #get the total time in seconds for start and target times
        targetTimeInSeconds = targetTime.hour * 3600 + targetTime.minute * 60 + targetTime.second
        startTimeInSeconds = self.startTime.hour * 3600 + self.startTime.minute * 60 + self.startTime.second

        #uses those times to figure out the possible distance
        possibleDistance = 0
        if(targetTimeInSeconds > startTimeInSeconds):
            possibleDistance = (targetTimeInSeconds - startTimeInSeconds) / 3600 * self.mph
        #print(self.startTime, "startTime")
        #print(possibleDistance, "possibleDistance")
        #now starts the real delivery
        self.deliver_packages(possibleDistance, orderFound)

    def deliver_packages(self, maxDistance, orderFound):
        """
        Where the delivery really starts.
        """
        currentDistance = 0.0
        order = list()
        for i in range(len(self.packages) + 1):
            calculatedDistance = -1
            #figures out which package to deliver
            deliveredPackage = self.pick_package(orderFound, order)
            calculatedDistance = LocationManager.get_distance(self.currentLocation.address.address, deliveredPackage.address.address)
            if(calculatedDistance != -1):
                #this is for setting packages to be enroute.
                if(not self.atHub and i < len(self.packages)):
                    deliveredPackage.set_enroute()
                
                #check if passed max distance
                if(currentDistance + calculatedDistance < maxDistance):
                    self.atHub = False
                    #deals with things only a package would know
                    if(i < len(self.packages)):
                        currentDistance += calculatedDistance
                        deliveredPackage.set_delivered(self.current_time(currentDistance))
                        self.currentLocation = deliveredPackage
                    #deals with going back to the hub
                    else:
                        self.currentLocation = deliveredPackage
                        currentDistance += calculatedDistance
                        self.returnedTime = self.current_time(currentDistance)
                        self.deliveredAll = True
                        self.atHub = True  
                else:
                    #packages
                    if(i < len(self.packages)):
                        self.currentLocation = deliveredPackage
                        #on_time_check is needed to ensure that onTime displays the correct value. 
                        #if its not delivered but still before the deadline then its not late.
                        currentDistance = maxDistance
                        deliveredPackage.on_time_check(self.current_time(currentDistance))
                    #hub
                    else:
                        self.currentLocation = deliveredPackage
                        currentDistance = maxDistance
                        self.deliveredAll = True
                        self.atHub = True  
            else:
                print("Calculated Distance failed in deliver packages", self.currentLocation.address.address,"|", deliveredPackage.address.address)
        self.packages = order
        self.distanceTraveled = currentDistance

    def pick_package(self, orderFound, orderedList = list()):
        """
        Picks the closest location based on packages in truck.\n
        only works with deliver packages since that changes the currentLocation and supplies the list.
        """
        #used to determine what is considered nearby for a package
        distanceClose = 1
        #deliveredPackage set to start location so it returns to hub after all packages are delivered.
        deliveredPackage = self.startLocation
        lowestDistance = math.inf
        #me being lazy
        lowestDeadline = Package().deadline
        for packageId in self.packages:
            #get package from package manager
            package = PackageManager.find_package(packageId)
            
            #checks if the package qualifies to be returned. 
            #if not continue to the next package.
            if(type(package) != Package):
                print("pick_package: package of id", packageId, "does not exist.")
                continue
            if(self.exists(orderedList,packageId)):
                continue

            #used when there is already a saved order
            if(orderFound):
                deliveredPackage = package
                break
            
            #picks the next package
            calculatedDistance = LocationManager.get_distance(self.currentLocation.address.address, package.address.address)
            if(calculatedDistance != -1):
                #checks if package is nearby
                if(calculatedDistance <= distanceClose and calculatedDistance < lowestDistance):
                    deliveredPackage = package
                    lowestDistance = calculatedDistance
                    lowestDeadline = package.deadline
                #check if deadline is less than the current lowest and something nearby has not already been picked.
                elif(package.deadline < lowestDeadline and lowestDistance > distanceClose):
                    deliveredPackage = package
                    lowestDistance = calculatedDistance
                    lowestDeadline = package.deadline
                #sorts packages of the same deadline based on distance
                elif(package.deadline <= lowestDeadline and calculatedDistance < lowestDistance):
                    deliveredPackage = package
                    lowestDistance = calculatedDistance
                    lowestDeadline = package.deadline
            else:
                print("Calculated Distance failed in pick_package", self.currentLocation.address.address,"|", deliveredPackage.address.address,"|", calculatedDistance)
                
        #the last value after delivering all packages should be a location which i do not want to be added.
        if(type(deliveredPackage) == Package):
            orderedList.append(deliveredPackage.id)
        return deliveredPackage

    def current_time(self, distance):
        """
        Converts distance to time and fires the check_time_events function in Events.
        """
        startTimeInSeconds = self.startTime.hour * 3600 + self.startTime.minute * 60 + self.startTime.second
        currentTimeInSeconds = int((distance / self.mph * 3600) + startTimeInSeconds)
        hour = int(currentTimeInSeconds // 3600)
        #print(distance)
        min = int((currentTimeInSeconds % 3600) // 60)
        sec = int((currentTimeInSeconds % 3600) % 60)
        currentTime = time(hour, min, sec)
        Events.check_time_events(currentTime)
        #print("current time:", currentTime)
        return currentTime
    

    def exists(self, packages : list, value):
        try:
            packages.index(value) 
            return True   
        except:
            return False 

    def __eq__(self, truck):
        if(truck == None):
            return False
        self.id == truck.id

    def has_space(self, package):
        if(type(package) == int):
            package = PackageManager.find_package(package)
        #I could check for whether its a Package type here but getting something other than a Package
        #should not happen. I'd much rather get an error here.
        return package.weight + self.currentWeight < self.maxWeight and len(self.packages) < self.maxPackages
    