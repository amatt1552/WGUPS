"""
Runs the code.\n
Author: Austin Matthews 001341371
"""
import math
import PackageManager
import LocationManager
import TruckManager
import UIManager
import Events
import os
import csv
import time

#----------------initializing variables and functions--------------

succeeded = False
order = list()
targetTime = "11:59 PM"
bestDistance = math.inf
app = None

def reset(usedWithButton = False):
    """
    Deletes order.csv if it exists and resets bestDistance.\n
    Source: https://www.w3schools.com/python/python_file_remove.asp
    """
    global bestDistance
    if os.path.exists("order.csv"):
        os.remove("order.csv")
        PackageManager.reset_packages()
        if(usedWithButton):
            app.set_data("Reset was successful.")
        else:
            print("Reset was successful.")
    else:
        if(usedWithButton):
            app.set_data("There's no file to delete!")
        else:
            print("There's no file to delete!")
    bestDistance = math.inf

def optimize_delivery(targetDistance = 120, maxTries = 2000, usedWithbutton = False):
    """
        Tries to find a better total distance.\n
        If bestDistance - 1 is > targetDistance it will only need to find a total distance less than the targetDistance.\n
        Else it finds a value that is <= bestDistance -1. 
    """
    global succeeded
    global targetTime
    global bestDistance
    i = 0
    succeeded = False

    if(usedWithbutton):
        app.set_data("Optimizing..")
    while(not succeeded and i < maxTries):
        #resets values
        Events.add_time_event("change address", "10:20 AM", 9, ", 410 S State St, Salt Lake City, UT, 84111")
        PackageManager.reset_packages()
        TruckManager.init_trucks()

        #tries to deliver before targetDistance
        succeeded = TruckManager.start_deliver_packages(targetTime, targetDistance)
        totalDistance = TruckManager.totalDistance
        #check is its less than bestDistance
        succeeded = succeeded and totalDistance <= bestDistance - 1

        i+=1
        #if succeeded set package order to order.csv.
        if(succeeded):
            with open("order.csv", "w", newline='') as writeFile:
                truckIndex=0
                while(TruckManager.get_packages(truckIndex) != None):
                    writer = csv.writer(writeFile, delimiter=",")
                    writer.writerow(TruckManager.get_packages(truckIndex))
                    truckIndex+=1
                bestDistance = totalDistance

                displayedResults = "Optimization succeeded in " + str(i) + " tries.\n"
                displayedResults += "New distance: " + "{:.2f}".format(bestDistance)
                if(usedWithbutton):
                    app.set_data(displayedResults)
                else:
                    print(displayedResults)
            break
        
        #debugging
        #if(i%100 == 0):
        #    print("Truck distances:")
        #    print(TruckManager.distance_traveled(0))
        #    print(TruckManager.distance_traveled(1))
        #    print(TruckManager.distance_traveled(2))

    if(usedWithbutton and not succeeded):
        app.set_data("Optimization Failed.")
    elif not succeeded:
        print("Optimization Failed.")

    print("Tries:", i)

def start_delivery(usedWithbutton = False):
    """
        Tries to deliver package based on order.csv. If it doesn't exist, runs optimize_delivery.
    """
    readFile = None
    global succeeded
    global targetTime
    global bestDistance

    if(usedWithbutton):
        targetTime = app.get_time()
    try:
        readFile = open("order.csv", "r")
        order.clear()
        i=0
        for line in csv.reader(readFile, delimiter = ','):
            #creates seperate list for each truck
            order.append(list())
            for value in line:
                order[i].append(int(value))
            i+=1
        #deliver based on the saved order
        Events.add_time_event("change address", "10:20 AM", 9, ", 410 S State St, Salt Lake City, UT, 84111")
        PackageManager.reset_packages()
        TruckManager.init_trucks(order)
        succeeded = TruckManager.start_deliver_packages(targetTime, 120, True)
        if(succeeded):
            bestDistance = TruckManager.totalDistance        
    except FileNotFoundError:
        #create a saved order if no file found
        if(usedWithbutton):
            app.set_data("File Not Found. Optimizing..")
        optimize_delivery()
    finally:
        if(readFile != None):
            readFile.close()
        if(usedWithbutton):
            app.set_data(TruckManager.status_of_deliveries())
        else:
            print(TruckManager.status_of_deliveries())

def start_look_up():
    """
    Used to find and print a list of packages.
    """
    searchedValue = app.get_lookup()
    if(type(searchedValue) == int):
        app.set_data(PackageManager.find_package(searchedValue))
    else:
        values = sorted(PackageManager.look_up(searchedValue), reverse=True)
        returnedValue = ""
        for value in values:
            returnedValue += str(value) + "\n"
        app.set_data(returnedValue)

def startup():
    PackageManager.set_packages()
    #input("press it")
    #print(PackageManager.find_package(10))
    #values = PackageManager.look_up(4)
    #for value in values:
    #    print(value)
    #input("press it")
    LocationManager.set_locations()
    #input("press it")
    #print(LocationManager.get_distance("1488 4800 S", "1060 Dalton Ave S"))
    #input("press it")

    start_delivery()

   

#--------------------Starts up code--------------------

startup()

#-------------------------UI--------------------------

runCommand = lambda:start_delivery(True)
optimizeCommand = lambda:optimize_delivery(usedWithbutton=True)
resetCommand = lambda:reset(True)
lookupCommand = start_look_up

app = UIManager.get_window(runCommand, optimizeCommand, resetCommand, lookupCommand)
app.set_data(
"""
Run displays results of delivery based on target time.\n
Optimize attempts to find a faster route for delivery.\n
Reset deletes the saved order alowing you to start from scratch.\n
Find Package(s) is used to find packages and is case sensitive.""")
app.mainloop()