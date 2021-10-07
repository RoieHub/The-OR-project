import  Request
import RTV_graph
import Vehicle
class Greedy_assingment:
   def __init__(self,rtv_g : RTV_graph):
      r_ok = {} # Set of assigned requests
      v_ok = {} # Set of vehicles with assigned trips

      # get all e(T,v) edges from rtv graph
      edges = rtv_g.graph.edges
      sorted_edges = sorted(rtv_g.graph.edges , key=edges )  #

      #sort edges by len(T)

      k = Vehicle.max_cap
      for t_size in range(k,1,-1):
         print("temp")







