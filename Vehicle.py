import datetime
import Request

"""The current state of a vehicle v is given by a tuple {current_position , current_time , passengers}
    A passenger p is a request that has been picked-up by a vehicle.
"""
class Vehicle:
    class_counter = 0
    max_cap = 10

    #TODO - the passengers parameter might be unused in all cases - when are we construting a vehicle and telling it - "you already have these passengers on you"?
    def __init__(self , start_node, passengers=None):
        self.id = Vehicle.class_counter
        Vehicle.class_counter += 1
        self.curr_time = datetime.datetime.now()
        self.curr_pos = start_node
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def __repr__(self):
        return self.id

    #This method returns the Node ID of the nearest node.
    def get_curr_pos(self):
        return self.curr_pos()

    def set_curr_pos(self,pos):
        self.curr_pos = pos
        return

    def add_passenger(self,req):
        self.passengers.append(req)
        return

    #This method removes the passenger object given to the func
    def rm_passenger(self, passenger):
        if self.passengers is not None :
            self.passengers.remove(passenger)
        return




