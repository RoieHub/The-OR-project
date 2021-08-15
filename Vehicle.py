import datetime
class Vehicle:
    cp : int # Current possition , location node.
    ct : datetime.datetime # Current time registered in the vehicle.
    passngers : list # Dynamic list of requests that been picked up by this vehicle.
