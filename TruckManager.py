"""
Handles Trucks and most delivery functions.
"""
from Truck import Truck
import PackageManager
import random
import math
from datetime import datetime

trucks = list()
usedPackages = list()
truckCount = 3
drivers = 2
totalDistance = 0

def init_trucks(savedOrder = None):
    usedPackages.clear()
    trucks.clear()
    #tries to find the optimal load order if nothing saved
    if(savedOrder == None):
        set_packages()
    
    #uses saved load order
    else:
        for i in range(truckCount):
            truck = Truck(i)
            truck.add_packages(savedOrder[i])
            trucks.append(truck)
    #sets the start time for truck 1 for late packages.
    trucks[1].startTime = "9:05 AM"

def set_packages():
    """
    Used to initialize packages in all trucks.
    """
    #--------------------------some initialization---------------------------
    #first decide where non eod packages with no requirements will go.
    #normally this would be figured out by some other method 
    #but i'm doing it manually to save time
    earlyPackages = list()
    earlyPackages.append(30)
    earlyPackages.append(31)
    earlyPackages.append(34)
    earlyPackages.append(1)
    earlyPackages.append(37)
    earlyPackages.append(40)
    earlyPackages.append(29)
    
    #initialize trucks
    for i in range(truckCount):
        truck = Truck(i)
        trucks.append(truck)

    #--------------------------adding special cases------------------------------------

    #truck 1   
    #together
    #14 15 19
    #16 13 19
    #20 13 15
    trucks[0].add_package(15)
    trucks[0].add_package(14)
    trucks[0].add_package(19)
    trucks[0].add_package(16)
    trucks[0].add_package(13)
    trucks[0].add_package(20)
    
    #truck 2
    #delayed
    trucks[1].add_package(25)
    trucks[1].add_package(6)
    trucks[1].add_package(28)
    trucks[1].add_package(32)
    #only truck 2
    trucks[1].add_package(3)
    trucks[1].add_package(18)
    trucks[1].add_package(36)
    trucks[1].add_package(38)

    #truck 3

    #---------------adds all early packages to trucks------------------------------
    while len(earlyPackages) > 0:
        
        #picks a random truck based on driver count or truck count if more drivers
        maxTrucks = drivers
        if(drivers > truckCount):
            maxTrucks = truckCount
        truckId = int(random.random() * maxTrucks)

        #picks a random package from early packages
        earlyPackagesId = int(random.random() * len(earlyPackages))
        trucks[truckId].packages.append(earlyPackages[earlyPackagesId])
        #adds to used packages then removes from earlyPackages
        usedPackages.append(earlyPackages.pop(earlyPackagesId))
    
    #---------------add all predetermined packages to used packages----------------------
    #together
    usedPackages.append(15)
    usedPackages.append(14)
    usedPackages.append(19)
    usedPackages.append(16)
    usedPackages.append(13)
    usedPackages.append(20)
    #other
    #usedPackages.append(30)
    #usedPackages.append(31)
    #usedPackages.append(34)
    #usedPackages.append(1)
    #usedPackages.append(37)
    #usedPackages.append(40)
    #usedPackages.append(29)
    #delayed
    usedPackages.append(25)
    usedPackages.append(28)
    usedPackages.append(32)
    usedPackages.append(6)
    #only truck 2
    usedPackages.append(3)
    usedPackages.append(18)
    usedPackages.append(36)
    usedPackages.append(38)

    #--------------------------handles the other packages--------------------------------
    while(len(usedPackages) < len(PackageManager.packages)):
        
        truckId = int(random.random() * truckCount)
        truck = trucks[truckId]
        packageId = int(random.random() * len(PackageManager.packages))+1
        if(not existsInUsed(packageId) and truck.has_space(packageId)):
            usedPackages.append(packageId)
            truck.add_package(packageId)
    

def start_deliver_packages(targetTime = "11:59 PM", targetMiles = 140, sortPackages = False):
    """
    Tries to deliver Packages while Determening which trucks deliver first.\n
    Return: Only returns True if completed within the targetTime and targetMiles.
    """
    drivenTrucks = list()
    global totalDistance
    totalDistance = 0
    firstBack = None
    shortestTime = datetime.strptime("11:59 PM","%I:%M %p").time()
    #i is for trucks
    i = 0
    while(i < len(trucks) and not trucks[i].deliveredAll):
        #j is for drivers
        j = 0
        while(j < drivers and i < len(trucks)):
            #this picks the first driver that returns assuming all have left.
            #You have to wait for their return before delivering for the other truck.
            if(i != 0 and i >= drivers):
                for truck in drivenTrucks:
                    if(truck.returnedTime == None):
                        break
                    if(truck.returnedTime < shortestTime and truck.atHub and truck.deliveredAll):
                        shortestTime = truck.returnedTime
                        firstBack = truck
                        #print("time", shortestTime)

            #this handles the first run of deliveries.
            if(i < drivers):
                trucks[i].start_delivery(targetTime, sortPackages)
                drivenTrucks.append(trucks[i])
                totalDistance += trucks[i].distanceTraveled
            #this handles the driver shortage.
            elif(firstBack != None):
                    trucks[i].startTime = firstBack.returnedTime
                    drivenTrucks.remove(firstBack)
                    trucks[i].start_delivery(targetTime, sortPackages)
                    drivenTrucks.append(trucks[i])
                    totalDistance += trucks[i].distanceTraveled
            #Debugging
            #print("truck", i)
            #PackageManager.print_by_id(trucks[i].packages)
            i += 1
            j += 1
    
    #check if succeeded.
    if(totalDistance > targetMiles):
        return False
    for truck in trucks:
        for packageId in truck.packages:
            package = PackageManager.find_package(packageId)
            if(not package.deliveryStatus.packageStatus.value == 3 or not package.deliveryStatus.onTime):
                return False
    
    return True

def status_of_deliveries():
    """
    Gives the status for both trucks and packages.
    """
    status = "Total Distance: " + "{:.2f}".format(totalDistance)
    for i in range(len(trucks)):
        status += "\nTruck " + str(i + 1) + " Packages:\n"
        try:
            status += "Start Time: " + str(trucks[i].startTime.strftime("%I:%M %p")) + "\n"
        except:
            status += "Start Time: " + str(trucks[i].startTime) + "\n"
        for package in trucks[i].packages:
            status += str(PackageManager.find_package(package)) + "\n"
        status +=  "Distance Traveled: " + "{:.2f}".format(distance_traveled(i)) + "\n"
        try:
            status += "Returned Time: " + str(trucks[i].returnedTime.strftime("%I:%M %p")) + "\n"
        except:
            status += "Returned Time: " + str(trucks[i].returnedTime) + "\n"
    return status

def distance_traveled(truckIndex):
    """
    Gets distance for a specific truck.
    """
    if(truckIndex < len(trucks)):
        return trucks[truckIndex].distanceTraveled

def get_all_packages():
    """
    Gets packages for all trucks.
    """
    newList = list()
    for truck in trucks:
        newList.extend(truck.packages)
    return newList

def get_packages(truckIndex):
    """
    Gets packages for a specific truck.
    """
    if(truckIndex < len(trucks)):
        return trucks[truckIndex].packages
    return None

def existsInUsed(id):
    try:
        usedPackages.index(id)
    except ValueError:
        return False
    return True
