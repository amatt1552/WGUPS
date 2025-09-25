"""
Handles Events like a change in address.
"""
from datetime import datetime
import PackageManager
class TimeEvent:
    def __init__(self, eventType, time, id, value) -> None:
        self.time = time
        self.eventType = eventType
        self.id = id
        self.value = value

timeEvents = list()
def add_time_event(eventType :str, time, id, value):
    if(type(time) == str):
        time = datetime.strptime(time ,"%I:%M %p").time()
        timeEvents.append(TimeEvent(eventType, time, id, value))
    
def check_time_events(currentTime):
    if(type(currentTime) == str):
        currentTime = datetime.strptime(currentTime ,"%I:%M %p").time()
    for event in timeEvents:
        if(str.lower(event.eventType) == "change address"):
            if(currentTime >= event.time):
                PackageManager.change_address(event.id, event.value)
                timeEvents.remove(event)
        else:
            print("There is no event type called", event.eventType)


    

