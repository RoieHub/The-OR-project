import itertools
import datetime


class Request:
    class_counter = 0
    max_waiting_time = datetime.timedelta(minutes=5)
    travel_delay = datetime.timedelta(minutes=15) # Max time that can be added to when the person making the request will reach their destination.
                                                  # This is used for calculating his max overall delay (i.e. if he had taken a private taxi when he made the request, travel_delay is how much time will verall be added to his delay, including waiting)

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
        self.latest_time_to_pick_up = self.time_of_request + max_waiting_time
        self.actual_pick_up_time=None
        self.estimated_dropoff_time = None  #Explanation - A value will be given to this when a vehicle wil be first assigned to him. If it is none when assigning a vehicle to him,
                                                            # the time a vehicle that wants to be assigned to it must be at least earliest_time_to_dest.
                                                            # else, meaning this (estimated_dropoff_time) is not none, it itself is the time to beat - so if a vehicle wants to be assigned to this request, it must be better then it.
        self.earliest_time_to_dest = self.time_of_request #TODO - add to this the time of shortest path from his origin to his destination.

    def __init__(self, ori, dest,request_time):
        self.id = Request.class_counter
        Request.class_counter += 1
        self.origin = ori
        self.destination = dest
        self.time_of_request = request_time
        self.latest_time_to_pick_up = self.time_of_request + datetime.timedelta(minutes=15)
        self.actual_pick_up_time = None
        self.estimated_dropoff_time = None  # Need to calc expected time to dropoff.
        self.earliest_time_to_dest = None


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









