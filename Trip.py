
"""
A trip T is a set of request that can be combined and served by a single vehicle.
A trip may have one or more candidate vehicles for  execution.
"""
from typing import Tuple

import Vehicle


class Trip:
    class_counter = 0

    def __init__(self, requests): #, candidate_v=None <-- removed. I don't think we need this - Ofir
                                # Also, requests was optional (i.e. requests=None). I changed that. No trip shuold be
                                # empty. I think requests should be given when creating the trip object,
                                # and shouldn't be changed. That means all requests should be known in advanced.
        self.id = Trip.class_counter
        Trip.class_counter +=1
        self.requests = requests
        self.v_candidates = []

    ''' - not needed. A trip will be created with it's requests when it is created, and they shouldn't be changed
    def add_request(self,req):
        self.requests.append(req)
        return
    '''

    def add_vehicle_candidate(self, VC: Tuple[Vehicle.Vehicle, int]): #VC = vehicle cost
        self.v_candidates.append(VC)

    def __repr__(self):
        # return ', '.join(self.requests)
        return str(self.requests)

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def __le__(self, other):
        return self.__repr__() <= other.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __ne__(self, other):
        return self.__repr__() != other.__repr__()

    def __gt__(self, other):
        return self.__repr__() > other.__repr__()

    def __ge__(self, other):
        return self.__repr__() >= other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())