
class Trip:
    requests : list # Set of requests that can be served by single vehicle.
    cv : list # Needed? Candidate vehicles for execution (May be more then one)

    def add_request(self,req):
        self.requests.append(req)
        return