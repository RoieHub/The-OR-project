import networkx as nx
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

class RV_graph :

    def __init__(self,req_lst,vehi_list):
       # Init an empty Graph
       self.graph = nx.Graph()
       # Should we first convert the requests and vehicles to nodes? or the graph does it anyway
       # Add all requests as nodes of type "r"
       self.graph.add_nodes_from(req_lst,type="r")
       self.graph.add_nodes_from(vehi_list, type="v")
       # Check every two nodes if they edge can be made




