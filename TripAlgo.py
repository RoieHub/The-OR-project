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
def travel(v: Vehicle, R: Tuple[Request, ...], sp_dict): #Request should be an array. Need to check how to do that.

    first_node = travel_node(_v=v, requests=R, sp_dict=sp_dict)

    threshold = len(first_node.current_possible_destinations) * Request.travel_delay # cost, or delay, caused with the best found route. It's max value can be (the amount of riders on the vehicle + amount of requests) * Request.travel_delay, so that is it's initial value. The initial threshold.
    best_route = []

    value = expand_tree(first_node, threshold)


#For each of the node's children (possible destinations) tries to expand the tree.
#Checking if already going over the threshold, or lowest extra_time_left on the possible destinations is negative (= fail)
def expand_tree(current_node: travel_node, t: int):
    found_an_answer = False
    threshold = t
    answer_route = []
    empty_answer = (False, -1, ())
    #check if already went over the threshold
    if current_node.accumulating_delay >= threshold:
        return empty_answer

    #check if the lowest extra_time_left value of the left possible destinations is negative - meaning this route is not relevant
    if current_node.current_possible_destinations[0][0] < 0:
        return empty_answer

    #if there are no more possible destinations, it means we have found a route, and it has lower cost (accumulating_delay) then the best we found so far
    if len(current_node.current_possible_destinations) == 0:
        return True, current_node.accumulating_delay, current_node.route

    #for each of the possible children of the node (i.e. going to one of the current_possible_destinations)
    # try to go there, and expand the tree further.
    for next_destination in current_node.current_possible_destinations:
        new_node = travel_node(_v = current_node.my_vehicle, requests = (), sp_dict=sp_dict, copy_me = current_node, destination_to_remove = next_destination)
        returned_value = expand_tree(new_node, threshold)
        if returned_value[0]==True:
            answer_route = returned_value[2]
            threshold = returned_value[1]
            found_an_answer = True

    if found_an_answer == False: #this is in case a (maybe better, maybe generally) route was not found
        return empty_answer
    else:
        return True, threshold, answer_route





class travel_node:
    """Nodes in the DFBnB tree, for the travel function"""
    #parent = null

    def __init__(self, _v: Vehicle, requests: Tuple[Request, ...], sp_dict, copy_me: travel_node=None,
                 destination_to_remove: Tuple[int, Request, char]=None):
        #destination_to_remove is a tuple of 1. The request that we now drove to, 2.A char with the value 'p' or 'd', to know if it is pickup or dropoff

        if copy_me is not None: #case of NOT initial node of the tree
            #save the previous location, copy the delay acumultaed untill now, and the route untill now and append to it the location you went to now
            self.previous_location = copy_me.current_location
            self.accumulating_delay = copy_me.accumulating_delay
            self.route = copy_me.route
            self.route.append((destination_to_remove[1], destination_to_remove[2]))

            # Check if the drive you just did was to pickup or to drop-off someone.
            # Added_time, the variable used to update the time left for all other "current_possible_destinations", will be set accordingly (according to the time taken to drive to the current location from the prev location).
            # Also, if it was a pickup, we need to add the same request, now as a drop-off, to the "current_possible_destinations".
            # But we will do this later, because we update all the "extra_time_left" values in the "current_possible_destinations" for all the nodes in the "current_possible_destinations" heap. That update is not needed for this
            # drop-off, and will make it have a wrong value

            # On the other hand ("else"), meaning this was a drop-off, we add the delay caused to this person to the "self.accumulating_delay" value.

            if destination_to_remove[2] == 'p':
                added_time = datetime.timedelta(seconds=sp_dict[copy_me.current_location][destination_to_remove[1].origin])
                self.current_location = destination_to_remove[1].origin
                self.time = copy_me.time + added_time

            else:
                added_time = sp_dict[copy_me.current_location][destination_to_remove[1].destination]
                self.time = copy_me.time + added_time
                self.current_location = destination_to_remove[1].destination

                #The time added to the accumulated dealy will be -
                # The time we got to it's dest (self.time) - the earilest time the person could have gotten to his\her dest, by driving alone (i.e. the delay he suffered by using our service - how much time was added to his journey because he used our service, and not driving alone at the time he requested)
                self.accumulating_delay += self.time - destination_to_remove[1].earliest_time_to_dest

            #set this node's vehicle to be the same as that of the node you are copying from
            #copy the current_possible_destinations as well, from the previous node, and remove the destination you just drove to
            self.my_vehicle = copy_me.my_vehicle
            self.current_possible_destinations = copy_me.current_possible_destinations
            self.current_possible_destinations.remove(destination_to_remove)

            #update the extra time left for all the tuples in the "current_possible_destinations" object.
            #Calculated like this -
            # 1. what they had before.
            # 2. add the time it would have taken to get from the prev location to them
            # 3. decrease the time it took to get from prev location to current location
            # 4. decrease the time it will take to get from the current location to the node's pickup\dropoff

            #After that, if we drove to a pickup, we will add that request's dropoff to the "current_possible_destinations" object

            # After that, re-sort
            for c in self.current_possible_destinations:
                if c[2] =='p':
                    c[0] = c[0] + sp_dict[previous_location][c[1].origin] - added_time - sp_dict[self.current_location][c[1].origin]
                else:
                    c[0] = c[0] + sp_dict[previous_location][c[1].destination] - added_time - sp_dict[self.current_location][c[1].destination]
                # c[0] = c[1]. self.time + sp_dict

            if destination_to_remove[2] == 'p':  # if the vehicle drove to a request, a pickup, add the drop-off to the current_possible_destinations
                #calculte the extra_time_left_to_drop-off, by taking the request's estimated_dropoff_time, subtract the "current" time (self.time, the time this vehicle would reach this current location) and subtract the time to drive
                # from current_location to the destination of the ndoe we picked up
                extra_time_left_to_dropoff = destination_to_remove[1].estimated_dropoff_time - self.time - sp_dict[self.current_location][destination_to_remove[0].destination]

                # heappush(self.current_possible_destinations, (extra_time_left_to_dropoff, destination_to_remove[0], 'd'))  #the 'd' is to say this is a drop-off
                self.current_possible_destinations.append((extra_time_left_to_dropoff, destination_to_remove[1], 'd'))

            # heapify(self.current_possible_destinations)
            self.current_possible_destinations.sort(key=operator.itemgetter(0))





        else: # copy_me==None:
            self.previous_location = None
            self.time = datetime().datetime.now()
            self.current_location = _v.curr_pos
            self.my_vehicle = _v
            self.current_possible_destinations = []
            self.route = []

            # self.accumulating_delay will accumulate the delays caused to the riders. We will add to it each time we get a person to their drop_off location.
            # Also, we will compare it to the threshold, the best we found so far (minimum delay after getting everyone to their destination).
            # That way, if at some point we surpass that, meaning the route\branch of the tree we are checking now, is worse then the best we found so far, we can cut it. Stop searching there, saving time searching the tree.
            self.accumulating_delay = 0

            #add all the requests as possible destinations, calculating time left to start going to that destination, using that as the value to compare for the heap

            # According to the article -
            # "If a request is matched to a vehicle at any given iteration, its latest pick-up time is reduced to the expected pick-up time by that vehicle..."
            # So we check for every request if it wasn't already matched to a vehicle before, i.e. if r.estimated_dropoff_time == None
            # If it wasn't, the extra_time_left_to_pickup will be set according to r.latest_time_to_pick_up
            # Otherwise, the request was already matched to a vehicle, and the "ti,e to beat" is r.latest_time_to_pick_up, which should be the time when the vehicle already
            # matched to that request planned to get to it.

            for r in requests:
                # extra_time_left_to_pickup = r.latest_time_to_pick_up - now
                if r.estimated_dropoff_time is None:
                    extra_time_left_to_pickup = r.latest_time_to_pick_up  - self.time #TODO minus time to get from vehicle's current location to request origin
                else: #in this case, a vehicle was already assigned
                    extra_time_left_to_pickup = r.estimated_dropoff_time - self.time #TODO minus time to get from vehicle's current location to request origin
                # heappush(self.current_possible_destinations, (extra_time_left_to_pickup, r, 'p')) #the 'p' is to say this is a pickup
                self.current_possible_destinations.append((extra_time_left_to_pickup, r, 'p')) #the 'p' is to say this is a pickup

            #add all the passangers currently on the vehicle as possible destinations, but this time calculate time left to start going their destinations (as they were already picked-up)
            for vr in _v.passengers:
                extra_time_left_to_dropoff = vr.estimated_dropoff_time - self.time #TODO minus time to get from vehicle's current location to passenger destination
                # heappush(self.current_possible_destinations, (extra_time_left_to_dropoff, vr, 'd')) #the 'd' is to say this is a drop-off
                current_possible_destinations.append((extra_time_left_to_dropoff, vr, 'd')) #the 'd' is to say this is a drop-off

            self.current_possible_destinations.sort(key = operator.itemgetter(0))





