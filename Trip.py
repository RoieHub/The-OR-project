
"""
A trip T is a set of request that can be combined and served by a single vehicle.
A trip may have one or more candidate vehicles for  execution.
"""
class Trip:
    class_counter = 0

    def __init__(self, requests=None, candidate_v=None):
        self.id = Trip.class_counter
        Trip.class_counter +=1
        if requests is None:
            self.requests = []
        if candidate_v is None:
            self.v_candidates = []

    def add_request(self,req):
        self.requests.append(req)
        return

    def __repr__(self):
        return ', '.join(self.requests)