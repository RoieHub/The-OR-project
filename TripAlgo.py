import Request
import networkx as nx
import datetime as dt


# Private case two requests (Mainly for RV graph)


"""
# This function simulates "virtual empty vehicle" that starts at r1 and , checks if picking up r2 is a valid option.
#returns : Boolean iff the !fastest! trip pass the constraints , String  : represents the !fastest! of the 3 trips 
example - 's1d1s2d2' this path first pick up goes to r1.source (s1) then drop r1 (d1) , pick's up r2 (s2) and drops r2 (d2)
This functoion only checks when r1 is picked up first.
# This  function uses exhaustive search ,  and can be improved
"""
def valid_trip2_min_cost(r1, r2, map,max_travel_delay):
    # Check both trips Z constraints

    # First we make sure that the first and most important condition is true
    # That is - if a virtual taxi, starting from r1 drives to r2, will it get
    # there in time? (i.e. - before r2.latest_time_to_pick_up)

    # Cacl travel times and time of arrival driving from r1 to r2
    # nx.algorithms.shortest_paths.generic.shortest_path_length
    r1S_to_r2S_pathDuration = nx.shortest_path_length(map, r1.origin, r2.origin, weight='travel_time')# d
    time_of_arrival_to_r2 = dt.datetime.now() + dt.timedelta(seconds=r1S_to_r2S_pathDuration)

    # This calculation might improve speed ,  as from all possible paths , path d allways followed by path e
    """"
    r2D_to_r1D_pathDuration = nx.shortest_path_length(map, r1.dest, r2.origin, weight='travel_time')  # e
    time_of_arrival_to_r2 = dt.datetime.now() + dt.timedelta(seconds=r1S_to_r2S_pathDuration)
    """""
    #in case we can't reach r2.origin in time
    if time_of_arrival_to_r2 > r2.latest_time_to_pick_up:
        return False , ''

    #now we need to check that a permutation exists where -
    # 1 - r2 doesn't wait until after his latest_time_to_pick_up
    # 2 - both r1 and r2 reach their respective destinations without

    #first we calculate all 6 possible steps in path.
    r1S_to_r1D_pathDuration = nx.shortest_path_length(map, r1.origin, r1.dest, weight='travel_time')# a

    r2S_to_r2D_pathDuration = nx.shortest_path_length(map, r2.origin, r2.dest, weight='travel_time')#c
    r2S_to_r1D_pathDuration = nx.shortest_path_length(map, r2.origin, r1.dest, weight='travel_time')#b

    #r1D_to_r2S_pathDuration = nx.shortest_path_length(map, r1.dest, r2.origin, weight='travel_time')#b


    r2D_to_r1D_pathDuration = nx.shortest_path_length(map, r2.dest, r1.dest, weight='travel_time')# e

    # the 'f' path is not needed when 'virtual vehicle' allways starts at r1S
    #r2D_to_r1S_pathDuration = nx.shortest_path_length(map, r2.dest, r1.origin, weight='travel_time') # f

    # Ver 1 exhaustive search

    # r1 r1 r2 r2
    p1 = r1S_to_r1D_pathDuration + r2S_to_r1D_pathDuration + r2S_to_r2D_pathDuration
    # r1 r2 r1 r2
    p2 = r1S_to_r2S_pathDuration + r2S_to_r1D_pathDuration + r2D_to_r1D_pathDuration
    # r1 r2 r2 r1
    p3 = r1S_to_r2S_pathDuration + r2S_to_r2D_pathDuration + r2D_to_r1D_pathDuration
    """
    # Is not needed when 'virtual vehicle' allways starts at r1S
    # r2 r2 r1 r1
    p4 = r2S_to_r2D_pathDuration + r2D_to_r1S_pathDuration + r1S_to_r1D_pathDuration
    # r2 r1 r2 r1
    p5 = r1S_to_r2S_pathDuration + r2D_to_r1S_pathDuration + r2D_to_r1D_pathDuration
    # r2 r1 r1 r2
    p6 = r1S_to_r2S_pathDuration + r1S_to_r1D_pathDuration + r2D_to_r1D_pathDuration
    
    """

    #shortest if only care of cost
    min_path=''
    min_t = min(p1, p2, p3)
    drop_r1 = 99999999
    drop_r2 = 99999999
    if min_t == p1:
        min_path = 's1d1s2d2'
        drop_r1 = r1.time_of_request + dt.timedelta(seconds=r1S_to_r1D_pathDuration)
        drop_r2 = r2.time_of_request + dt.timedelta(seconds=p1)

    if min_t == p2:
        min_path = 's1s2d1d2'
        drop_r1 = r1.time_of_request + dt.timedelta(seconds=(p2 - r2D_to_r1D_pathDuration))
        drop_r2 = r2.time_of_request + dt.timedelta(seconds=p2)

    else:
        min_path = 's1s2d2d1'
        drop_r1 = r2.time_of_request + dt.timedelta(seconds=p3)
        drop_r2 = r2.time_of_request + dt.timedelta(seconds=p3 - r2D_to_r1D_pathDuration)


    # checking second constraint passengers maximum travel delay
    # Formal constraint • For each request or passenger r, its maximum travel delay drop_r'i' ≤ r'i'.time_of_request + rs'i' to rd'i' + ∆.
    # t ∗ r = t rr + τ (o r , d r ).
    if drop_r1 <= r1. r1.time_of_request + dt.timedelta(seconds=r1S_to_r1D_pathDuration) + max_travel_delay and drop_r2 <= r1.time_of_request + dt.timedelta(seconds=r2S_to_r2D_pathDuration) + max_travel_delay  :
        return True , min_path
    else :
        return False , min_path
    ### TO DO! the fastest path might not pass the second check while ,  slower path might. or is it?






    return False
# simple phelper function that returns path to the minimum cost trip.
def path_builder(p1,p2,p3) :
    min_t = min(p1 , p2 ,p3)
    if min_t == p1 :
        return p1,'s1d1s2d2'
    if min_t == p2 :
        return p2,'s1s2d1d2'
    else :
        return p3,'s1s2d2d1'

#using DFBnB for travel
def travel(v: Vehicle, R: Request): #Request should be an array. Need to check how to do that.
    best_cost = -1 #cost, or delay, caused with the best found route
    best_route = []



class travel_node:
    """Nodes in the DFBnB tree, for the travel function"""
    #parent = null

    def __init__(self, v: Vehicle, requests: Tuple[Request, ...], copy_me: travel_node=None, destination_to_remove: Tuple[int, Request, char]=None):
        if copy_me!=None:
            self.time = copy_me.time #TODO + time to get from v.current_location to destination_to_remove[1].destination
            self.my_vehicle = copy_me.my_vehicle
            self.current_possible_destinations = copy_me.current_possible_destinations

            self.current_location = destination_to_remove[1].destination
            if destination_to_remove[2]=='p': #if the vehicle drove to a request, a pickiup, add the dropoff to the current_possible_destinations
                extra_time_left_to_dropoff = destination_to_remove[1]


        else: # copy_me==None:
            self.time = datetime().datetime.now()
            self.current_location = v.curr_pos
            self.my_vehicle = v
            self.current_possible_destinations = []

            #add all the requests as possible destinations, calculating time left to start going to that destination, using that as the value to compare for the heap

            # According to the article -
            # "If a request is matched to a vehicle at any given iteration, its latest pick-up time is reduced to the expected pick-up time by that vehicle..."
            # So we check for every request if it wasn't already matched to a vehicle before, i.e. if r.estimated_dropoff_time == None
            # If it wasn't, the extra_time_left_to_pickup will be set according to r.latest_time_to_pick_up
            # Otherwise, the request was already matched to a vehicle, and the "ti,e to beat" is r.latest_time_to_pick_up, which should be the time when the vehicle already
            # matched to that request planned to get to it.

            for r in requests:
                # extra_time_left_to_pickup = r.latest_time_to_pick_up - now
                if r.estimated_dropoff_time == None:
                    extra_time_left_to_pickup = r.latest_time_to_pick_up  - self.time #TODO minus time to get from vehicle's current location to request origin
                else: #in this case, a vehicle was already assigned
                    extra_time_left_to_pickup = r.estimated_dropoff_time - self.time #TODO minus time to get from vehicle's current location to request origin
                heappush(self.current_possible_destinations, (extra_time_left_to_pickup, r, 'p')) #the 'p' is to say this is a pickup

            #add all the passangers currently on the vehicle as possible destinations, but this time calculate time left to start going their destinations (as they were already picked-up)
            for vr in v.passengers:
                extra_time_left_to_dropoff = vr.estimated_dropoff_time - self.time #TODO minus time to get from vehicle's current location to passenger destination
                heappush(self.current_possible_destinations, (extra_time_left_to_dropoff, vr, 'd')) #the 'd' is to say this is a dropoff






