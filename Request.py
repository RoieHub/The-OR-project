import itertools
import datetime


class Request:
    class_counter = 0
    """"id: int
    origin: int   # Origin Node ID
    destination: int #  Destination Node ID
    time_of_request: datetime.datetime   #TimeOfRequest#
    latest_time_to_pick_up: datetime.datetime  #TimeOfLastPickup - latest time avilable for pickup# Default = time_of_request + Sim_init.max_delay
    actual_pick_up_time: datetime.datetime  #TimeOfPickup - called pickup time in the article. The time the request was actually picked up.#
    estimated_dropoff_time: datetime.datetime  #TimeOfExpextedDropoff -  expected drop off time#
    earliest_time_to_dest: datetime.datetime  #TimeOfEarliest - the earliest possible time at which the destination could be reached#"""

        #Dest and Ori constructor , defaultive 15 mins waiting.#
    def __init__(self , ori , dest ):
        self.id = Request.class_counter
        Request.class_counter += 1
        self.origin = ori
        self.destination = dest
        self.time_of_request = datetime.datetime.now()
        self.latest_time_to_pick_up = self.time_of_request + datetime.timedelta(minutes=15)
        self.actual_pick_up_time=None
        self.estimated_dropoff_time=None  #Need to calc expected time to dropoff.
        self.earliest_time_to_dest=None


    def update_actual_pick_up_time(self, puTime):
        self.actual_pick_up_time = puTime
        # !!!!!!!!!!!!!!Request should now change because its picked up!!!!!
        return

    def update_dropoff_time(self,dfTime):
        self.estimated_dropoff_time = dfTime
        return

    # Time to dest is T(Origin,Destination) time, we add it to time of request and get the earliest time to dest.
    def update_earliest_time_to_dest(self,time_to_dest):
        self.time_of_request+time_to_dest
        return






