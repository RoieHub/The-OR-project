
class Trip:
    class_counter = 0
    def __init__(self,reqsts=None,candidte_v=None):
        self.id = Trip.class_counter
        Trip.class_counter +=1
        if reqsts is None:
            self.requests = []
        if candidte_v is None:
            self.v_candidates = []



    def add_request(self,req):
        self.requests.append(req)
        return