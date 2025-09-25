import os
import csv
from Location import Location
from ModHash import ModHash

locations = ModHash()

def set_locations():
    """
        Sets locations based on the DistanceTable file.\n
        Source: #https://docs.python.org/3/library/csv.html
    """

    global locations
    file = None
    j = 0

    try:
        #find file
        file = open("DistanceTable.csv", "r")
        
        locationsAsList = list()
        count = 0
        for line in csv.reader(file, delimiter = ','):
            for i in range(len(line)):
                if(j == 0):
                    if(i >= 2):
                        count += 1
                else:
                    break
        locations = ModHash(count)
        file.seek(0)
        #read line
        for line in csv.reader(file, delimiter = ','):
            address = ""
            #assign values
            for i in range(len(line)):
                if(j == 0):
                    if(i >= 2):
                        #add base locations
                        location = Location(line[i],0, count)
                        locations.add(location)
                        locationsAsList.append(location)
                else:
                    #set target address
                    if(i == 0):
                        address = line[i]
                    elif(i == 1):
                        if(line[i] != " HUB"):
                            address += line[i]
                    #add target location
                    else:
                        addedLocation = Location(address,float(line[i]),count)
                        
                        locationAddedTo = locations.find(locationsAsList[i - 2].address.address)
                        locationAddedTo.add_target(addedLocation)
                if(line[i] == "0"):
                    break        
            j += 1
    except FileNotFoundError:
        print("LocationManager's set_locations function failed. Make sure you have a file named DistanceTable.csv")
    finally:
        if(file != None):
            file.close()

def get_distance(currentAddress, targetAddress) -> float:
    """
        Gets distance by comparing currentAddress and targetAddress to DistanceTable.\n
        Return: returns -1 if not found
    """
    #tries to find the currentLocation based on currentAddress.
    currentLocation = locations.find(currentAddress)
    if(type(currentLocation) == Location):
        #if found tries to find the targetLocation based on targetAddress.
        targetLocation = currentLocation.targetLocations.find(targetAddress)
        if(type(targetLocation) == Location):
            #if found, returns the distance.
            return targetLocation.distance
    #tries the inverse
    currentLocation = locations.find(targetAddress)
    if(type(currentLocation) == Location):
        targetLocation = currentLocation.targetLocations.find(currentAddress)
        if(type(targetLocation) == Location):
            return targetLocation.distance
    
    print("LocationManager's get_distance function failed. currentLocation:", currentLocation, "targetLocation:", targetAddress)
    return -1
    
    
