import  Request
import RTV_graph
import Vehicle
class Greedy_assingment:
   """
   Assuming RTV_graph.tao is a 2dMatrix of type trip
   """
   def __init__(self,rtv_g : RTV_graph):
      r_ok = {} # Set of assigned requests
      v_ok = {} # Set of vehicles with assigned trips

      # Creating the stack of e(T,v) edges representation.
      stack = []
      tao_len = len(RTV_graph.tao)

      # 1) Extracting all candidate vehicles with cost as they represent e(T,v)
      vc_tuples = []
      # For each set of trips of len k, from Tao.
      for k in range(1,tao_len) :
         # Extract (V,cost) tuple from each trip.
         vc_tuples.clear() # clears the container from the prev vc.
         for t in RTV_graph.tao[k] : # For each trip
            for vc in t.v_candidates : # Append the candidate (v,cost) to vc_tuples.
               vc_tuples.append((t.id,)+vc) # This is tuple concatenate so it will look as (t.id,v,cost)
         # Sort the vc by cost.
         vc_tuples.sort(key = lambda x: x[2])
         # Append each vc in reverse into our stack.
         for vc in reversed(vc_tuples):
            stack.append(vc)


      # At this point , our stack is filled with (trip.id , v , )


















