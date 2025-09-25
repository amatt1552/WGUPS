
class ModHash:
    """
        A very basic hash and storage solution.
    """
    def __init__(self, size = 33):
        self.mod = size
        self.buckets = [None] * self.mod
        self.length = 0
	
    #O(1)
    def add(self, item):
        id = item.id
        if(type(item.id) == str):
            id = self.string_to_int(item.id)

        if(type(id) != int):
            print("ModHash's add function only accepts ints and strings.\nMake sure you have an id set for item.")
            return
        #print(id)
        i = id % self.mod
        if(self.buckets[i] == None):
            self.buckets[i] = list()
        self.buckets[i].append(item)
        self.length += 1
        #print(len(self.buckets[i]))

	#O(1) best case O(n) worst case
    def remove(self,  item):
        id = item.id
        if(type(item.id) == str):
            id = self.string_to_int(item.id)

        if(type(id) != int):
            print("ModHash's remove function only accepts ints and strings.\nMake sure you have an id set for item.")
            return

        i =  id % self.mod
        
        self.buckets[i].remove(item)
        self.length -= 1

	#O(1) best case O(n) worst case
    def find(self, id):
        """
        Return: returns none if not found.
        """
        #numId is used to find the index while keeping the passed id intact
        numId = id
        if(type(id) == str):
            numId = self.string_to_int(id)

        if(type(numId) != int):
            print("This hash only accepts ints and strings")
            return
        #print(numId)
        i = numId % self.mod

        #once i is set, tries to find within the list in the bucket. 
        if(self.buckets[i] != None):
            for item in self.buckets[i]:
                #print(item.id, id, i)
                if(item.id == id):
                    return item
        else:
            return None
	
    def exists(self, id):
        numId = 0
        if(type(id) == str):
            numId = self.string_to_int(id)

        if(type(numId) != int):
            print("This hash only accepts ints and strings")
            return False
        #print(id)
        i = numId % self.mod
        try:
            for item in self.buckets[i]:
                #print(item.id)
                if(item.id == id):
                    return True
        except IndexError:
            print("something went wrong with the id.")
            return False
        return False

    def string_to_int(self, string) -> int:
        """
        Source: https://learn.zybooks.com/zybook/WGUC950AY20182019/chapter/7/section/6
        """
        stringHash = 5381 
       
        for char in string:
            stringHash = int((stringHash * 33) + ord(char))
        
        return stringHash
    
    def get_list(self):
        returnedList = list()
        for bucket in self.buckets:
            #print(len(bucket))
            for value in bucket:
                returnedList.append(value)
                   
        #print(len(returnedList))
        return returnedList
    
    def __len__(self):
        return self.length

    #Makes modhash iterable
    #https://www.w3schools.com/python/python_iterators.asp

    def __iter__(self):
        self.i = 0
        self.j = 0
        return self

    def __next__(self):
        if(self.i < len(self.buckets)):
            
            if(self.j < len(self.buckets[self.i])):
                self.j += 1
                
                return self.buckets[self.i][self.j-1]
            else:
                self.i += 1
                self.j = 0
            
        else:
            raise StopIteration 

