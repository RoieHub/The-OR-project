import  Request
import RTV_graph
import Vehicle
class Greedy_assingment:
   def __init__(self,rtv_g : RTV_graph):
      r_ok = {} # Set of assigned requests
      v_ok = {} # Set of vehicles with assigned trips
      trips = self.

      # get all e(T,v) edges from rtv graph
      edges = rtv_g.graph.edges(data=True) # HOW to take only edges of type e(T,v) ?
      sorted_edges = sorted(edges , key=len(edges[0])) #
      # vehicle_nodes = [x for x,y in rv_graph.nodes(data=True) if y['type'] == 'v']
      etv_edges =

      #sort edges by len(T) S k := sort e(T, v) in increasing cost, ∀T ∈ T k , v ∈ V

      k = Vehicle.max_cap
      for t_size in range(k,1,-1):
         print("temp")
        # while S k ! = ∅ do
        #   pop e(T, v) ← Sk
        #   if ∀r ∈ T, r ∈/ R ok and v ∈/ V ok then
        #      R ok ← {∀r ∈ T }; V ok ← v







