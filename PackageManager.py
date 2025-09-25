"""
Handles all packages.
"""
from Address import Address
from ModHash import ModHash
from Package import Package
import copy

packages = ModHash()
distanceTotal = 0

def set_packages():
    """
    Sets packages based on PackageFile.csv.
    """
    global packages
    file = None
    try:
        file = open("PackageFile.csv", "r")
        count = 0
        #get count
        for line in file:
            count += 1
        packages = ModHash(count)
        file.seek(0)
        #add to packages
        for line in file:
            values = line.split(",")
            package = Package(int(values[0]),values[1],values[2],values[3],values[4],values[5],int(values[6]),values[7])
            #print(str(package))
            packages.add(package)
    except FileNotFoundError:
        print("PackageFile.csv not found.")
    finally:
        if(file != None):
            file.close()

def change_address(id, value):
    package = packages.find(id)
    if(type(package) == Package):
        package.change_address(value)
    else:
        print("PackageMangager Could not change address..")

def find_package(id):
    """
        Used when you already know the id.\n
        Return: returns None if not found.
    """
    return packages.find(id)

def look_up(value):
    """
    Used to find a group of packages based on passed value.\n
    Utilizes __eq__ in Package, Address, and Package.DeliveryStatus.\n
    Return: returns a list of packages or None.
    """
    returnedValues = list()
    for package in packages:
        if(package == value):
            returnedValues.append(package)
    return returnedValues

def print_by_id(ids):
    value = ""
    for id in ids:
       value += str(packages.find(id)) + "\n"
    print(value)

def reset_packages():
    for package in packages:
        if(package != None):
            package.set_at_hub()
            package.address = copy.copy(package.oldAddress)
