
"""
A trip T is a set of request that can be combined and served by a single vehicle.
A trip may have one or more candidate vehicles for  execution.
"""
class Trip:
    class_counter = 0

    def __init__(self, requests=None): #, candidate_v=None <-- removed. I don't think we need this - Ofir
        self.id = Trip.class_counter
        Trip.class_counter +=1
        if requests is not None:
            self.requests = requests
        else:
            self.requests = []
        # if candidate_v is not None:
            # self.v_candidates = candidate_v
        # else:
            # self.v_candidates = []


    def add_request(self,req):
        self.requests.append(req)
        return

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