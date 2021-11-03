import datetime
import Request

"""The current state of a vehicle v is given by a tuple {current_position , current_time , passengers}
    A passenger p is a request that has been picked-up by a vehicle.
"""
class Vehicle:
    class_counter = 0
    max_capacity = 10

    def __init__(self , start_node, passengers=None, time=None):
        self.id = Vehicle.class_counter
        Vehicle.class_counter += 1
        self.r_connected_to_me = [] # Requests connected to me in the RV graph , use to improve running time. (Must be cleared AFTER EACH EPOCH!)
                                    # Will be made of triplets - The request, cost of path found for it (including just that request AND passengers already on the vehicle), and the path found for it.
        if time is not None:
            self.curr_time = time
        else:
            self.curr_time = datetime.datetime.now()

        self.curr_pos = start_node
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

        self.path = None # This will be used to store the path the vehicle has remaining from the last epoch, that he didn't have time tp finish. We use it in case the vehicle will not get a trip assigned to him on the next epoch, but still have passengers on him.

    def __repr__(self):
        return 'v' + str(self.id)

    def __hash__(self):
        return hash(self.__repr__())

    #This method returns the Node ID of the nearest node.
    def get_curr_pos(self):
        return self.curr_pos()

    def set_curr_pos(self,pos):
        self.curr_pos = pos
        return

    def add_passenger(self, req):
        self.passengers.append(req)
        return

    #This method removes the passenger object given to the func
    def remove_passenger(self, passenger):
        if self.passengers is not None:
            self.passengers.remove(passenger)
        return

    #This metod add a request to 'rv_to_me' dictionary, for rtv usage later.
    #def add_r_connected_to_me(self, r: Request, cost: int, path: list[tuple[Request, str]]): # This makes problems
    def add_r_connected_to_me(self, r: Request, cost: int, path):
        # self.r_connected_to_me[str(r)] = cost
        self.r_connected_to_me.append([r, cost, path])
    def clear_rv_after_epoch(self):
        self.r_connected_to_me.clear()



    def __lt__(self, other):
        return self.id < other

    def __le__(self, other):
        return self.id <= other

    def __eq__(self, other):
        return "v" + str(self.id) == other

    def __ne__(self, other):
        return self.id != other

    def __gt__(self, other):
        return self.id > other

    def __ge__(self, other):
        return self.id >= other




