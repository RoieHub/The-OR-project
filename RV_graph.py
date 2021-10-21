import copy
import datetime
from typing import Tuple
import networkx as nx
import Request
import TripAlgo
import Vehicle

"""
C. Pairwise graph of vehicles and requests (RV-graph)
The first step of the method is to compute (a) which requests can be pairwise combined, and (b) which
vehicles can serve which requests individually, given their current passengers. This step builds on the idea
of share-ability graphs proposed by [6], but it is not limited to the requests and includes the vehicles at
their current state as well.
Two requests r 1 and r 2 are connected in the graph if they can potentially be combined. This is, if
a virtual vehicle starting at the origin of one of them could pick-up and P drop-off both requests while
satisfying the constraints Z of maximum waiting time and delay. A cost
(t dr − t ∗ r ) can be associated
r={1,2}
to each edge e(r 1 , r 2 ).
Likewise, a request r and a vehicle v are connected if the request can be served by the vehicle while
satisfying the constraints Z. This is, if travel(v, r) returns a valid trip that drops the current passengers
of the vehicle and the picked request r within the specified maximum waiting and delay times. The edge
is denoted by e(r, v).
Limits on the maximum number of edges per node can be imposed, trading-off optimality at the later
stages. Speed-ups such as the ones proposed in T-share [4] could be employed in this stage to prune the
most likely vehicles to pick up a request.
This graph, denoted RV-graph, gives an overview of which requests and vehicles might be shared. In
Figure 3 an example of the RV-graph is shown with 90 requests and 30 vehicles

"""


class RV_graph:
    # TODO - when initiating  the program, create a virtual vehicle. It will be the premenant virtual vehicle, used all throught the running of the program.
    # current_time will be passed to this function. It can eoither be actual datetime.datetime.now, or some time given by a simulated run
    def __init__(self, requests_list: Tuple[Request.Request, ...], vehicle_list: Tuple[Vehicle.Vehicle, ...], virtual_vehicle: Vehicle, map_graph: nx.Graph, current_time: datetime ,spc_dict: dict):
        self.map_graph = map_graph
        # Init an empty Graph
        self.graph = nx.Graph()
        # Should we first convert the requests and vehicles to nodes? or the graph does it anyway
        # Add all requests as nodes of type "r"
        self.graph.add_nodes_from([(v, {'data': v, 'type':'v'}) for v in vehicle_list])
        self.graph.add_nodes_from([(r, {'data': r, 'type':'r'}) for r in requests_list])
        # self.graph.add_nodes_from(req_lst,type="r")
        # self.graph.add_nodes_from(vehi_list, type="v")
        self.rvEdge = None
        self.rrEdge = None
        # Check every two nodes if they edge can be made

        # Example of how to go to \ address a certain node -
        #   self.graph.nodes[some_vehicle.id]['data'].curr_pos

        # Create R->R edges in the graph
        # Complying with the article we are based on, this is done by sending each pair if requests to the travel() function.
        # If it can find a route for both of them, where a virtual empty vehicle starts at the location of one of them, then add an edge
        #  between them in the graph, weighted with the delay the aforementioned route has.
        # Otherwise, meaning a route couldn't be found, don't add an edge between them.
        for i in range(len(requests_list) - 1):
            for j in range(i + 1, len(requests_list)):
                # We create a copy of the 2 requests. so as not to change the originals
                first_req = copy.copy(requests_list[i])
                second_req = copy.copy(requests_list[j])

                # we update the first req to be picked up
                first_req.actual_pick_up_time = current_time
                time_already_waited = current_time - first_req.time_of_request
                first_req.estimated_dropoff_time = first_req.earliest_time_to_dest + Request.Request.travel_delay - time_already_waited # TODO - Is this needed or valid?

                # Then we update the virtual vehicle -
                #  set the virual vechicle to be at the request i, with that request boarded on him

                # virtual_vehicle.curr_time = current_time # TODO - decide if this is needed

                virtual_vehicle.curr_pos = first_req.origin
                virtual_vehicle.passengers = [first_req]

                returned_value = TripAlgo.travel(v=virtual_vehicle, R=(second_req,), map_graph=self.map_graph, spc_dict=spc_dict, current_time=current_time)
                if returned_value[0] == True:
                    self.graph.add_edge(first_req, second_req, weight=returned_value[1])  # TODO - decide if need the weight attribute here, and also if we need the route, which can be added (it is returned_value[2])


        # Next, we add an edge between vehicles and requests - to indicate what vehicles could possibly take which requests.
        # This is done by sending the vehicle and the single request to the travel() function.
        # If a route can be found, add an edge between that vehicle and the request in the graph, otherwise don't.
        for i in range(len(vehicle_list)):
            for j in range(len(requests_list)):
                current_vehicle = vehicle_list[i]
                current_request = copy.copy(requests_list[j])

                returned_value = TripAlgo.travel(v=virtual_vehicle, R=(current_request,), map_graph=self.map_graph, spc_dict=spc_dict, current_time=current_time)
                if returned_value[0] == True:
                    self.graph.add_edge(vehicle_list[i], requests_list[j], weight=returned_value[1])



def make_rv_rr_edges(self):
    # This mathod need to go over all nodes and create the appropriate rr and rv edges.
    return True
