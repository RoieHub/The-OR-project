import datetime


class Request:
    origin: int   # networx-node(pointer?)
    destination: int
    tor: datetime.datetime   #TimeOfRequest#
    tolp: datetime.datetime  #TimeOfLastPickup - latest time avilable for pickup#
    top: datetime.datetime  #TimeOfPickup - called pickup time in the article. The time the request was actually picked up.#
    toed: datetime.datetime  #TimeOfExpextedDropoff -  expected drop off time#
    toe: datetime.datetime  #TimeOfEarliest - the earliest possible time at which the destination could be reached#

        #Dest and Ori constructor , defaultive 15 mins waiting.#
    def __init__(self , ori , dest ):
        self.origin = ori
        self.destination = dest
        self.tor = datetime.datetime.now()
        self.tolp = self.tor + datetime.timedelta(minutes=15)
        self.toed = None  #Need to calc expected time to dropoff.
        self.toe = None


    def UpdateTOED(self , expected_drop_off_time):
        self.toed = expected_drop_off_time

    def UpdateTOE(self , time_of_earliest):
        self.toed = time_of_earliest




