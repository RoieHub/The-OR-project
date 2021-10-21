import  Request
import RTV_graph
import Vehicle

"""
This class recives a RTV_graph ,  and greedly assing trips to vehicles by the least cost.
public attributes :
@ assigned_tv : a set of assigned_tv tuples  (Type: Trip t ,Vehicle v,Possitve number cost )
 usefull to extract the exact assingments by the algo.
@ r_ok:  a set of request that are assinged by our algo.
@ v_ok: a set of vehicles that got new trips assinged to them.

!!!!! The class does not update any other class at all.
so the object of vehicle does NOT know what requests are assinged to it , this class only holds "assigned_tv"
so object need to be updated by this elsewhere.
!!!!!
"""

class Greedy_assingment:
   """
   Assuming RTV_graph.tao is a 2dMatrix of type trip
   """
   def __init__(self,rtv_g : RTV_graph):
      self.r_ok = {} # Set of assigned requests
      self.v_ok = {} # Set of vehicles with assigned trips
      self.assigned_tv = {}
      self.greedy_sum = 0

      # Creating the stack of e(T,v) edges representation.
      stack = []
      tao_len = len(rtv_g.tao)

      # 1) Extracting all candidate vehicles with cost as they represent e(T,v)
      vc_tuples = []
      # For each set of trips of len k, from Tao in decensding order.
      for k in range(tao_len-1,-1,-1) :
         # Extract (V,cost) tuple from each trip.
         vc_tuples.clear() # clears the container from the prev vc.
         for t in rtv_g.tao[k] : # For each trip
            for vc in t.v_candidates : # Append the candidate (v,cost) to vc_tuples.
               vc_tuples.append((t,)+vc) # This is tuple concatenate so it will look as (t.id,v,cost)

         # Sort the vc by cost.
         vc_tuples.sort(key = lambda x: x[2])
         # Append each vc in reverse into our stack.
         for vc in reversed(vc_tuples):
            stack.append(vc)

         # At this point , our stack is filled with (trip , v , cost ) of size k
         while len(stack) > 0:
            trip_tuple = stack.pop()
            if self.unassinged_trip(trip_tuple):
               for r in trip_tuple[0].requests:
                  self.r_ok.add(r)
               self.v_ok.add(trip_tuple[1])
               self.greedy_sum += trip_tuple[2]
               self.assigned_tv.add((trip_tuple))

   """
   This method checks if it is valid to assign a certain trip.
   @ trip_tuple: is a tuple containing (trip,v,cost)
   @ returns: False if the v (trip_tuple[1]) allready exist in self.v_ok.
            or if any request in trip.requests(trip_tuple[0].requests) is allready in r_ok.
            else return True
   """
   def  unassinged_trip(self,trip_tuple):
      # Check if v in self.v_ok
      if trip_tuple[1] in self.v_ok:
         return False
      else:
         # Check if are request is allready in r_ok.
         for r in trip_tuple[0].requests:
            if r in self.r_ok:
               return False
      return True



























