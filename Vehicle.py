import datetime
import Request
class Vehicle:
    #Vehicle id? - may be added
    class_counter = 0
    cp : int # Current possition , location node.
    ct : datetime.datetime # Current time registered in the vehicle.
    passengers : list # Dynamic list of requests that been picked up by this vehicle.

    def __init__(self , start_node):
        self.id = Vehicle.class_counter
        Vehicle.class_counter += 1
        self.ct = datetime.datetime.now()

    #This method returns the Node ID of the nearest node.
    def curr_pos(self):
        return self.cp
    def add_passenger(self,req):
        self.passengers.append(req)

    def __str__(self):
      #  print [str(Request.id) for p in self.passengers]
        return


