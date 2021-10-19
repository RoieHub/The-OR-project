from __future__ import annotations

import copy
import datetime
import operator
from typing import Tuple

import networkx

import Request
import Vehicle
import spc_dict_caregiver


class travel_node:
    """Nodes in the DFBnB tree, for the travel function"""
    #parent = null

    def __init__(self, _v: Vehicle, requests: Tuple[Request, ...], map_graph: networkx.Graph, spc_dict, copy_me: travel_node=None,
                 destination_to_remove: Tuple[int, Request, str]=None):
        #destination_to_remove is a tuple of 1. The request that we now drove to, 2.A char with the value 'p' or 'd', to know if it is pickup or dropoff

        if copy_me is not None: #case of NOT initial node of the tree
            #save the previous location, copy the delay acumultaed untill now, and the route untill now and append to it the location you went to now
            self.previous_location = copy.copy(copy_me.current_location)
            self.accumulating_delay = copy.copy(copy_me.accumulating_delay)
            self.route = copy.copy(copy_me.route) #TODO - I think a shallow copy, like it is now, is OK here, but need to make sure
            self.route.append((destination_to_remove[1], destination_to_remove[2]))

            # Check if the drive you just did was to pickup or to drop-off someone.
            # Added_time, the variable used to update the time left for all other "current_possible_destinations", will be set accordingly (according to the time taken to drive to the current location from the prev location).
            # Also, if it was a pickup, we need to add the same request, now as a drop-off, to the "current_possible_destinations".
            # But we will do this later, because we update all the "extra_time_left" values in the "current_possible_destinations" for all the nodes in the "current_possible_destinations" heap. That update is not needed for this
            # drop-off, and will make it have a wrong value

            # On the other hand ("else"), meaning this was a drop-off, we add the delay caused to this person to the "self.accumulating_delay" value.

            # We call the spc_dict_caregiver to make sure the shortest paths from the last node are already in the spc_dict. (If it is, it continues, otherwise it calcs and adds it).
            spc_dict_caregiver.spc_dict_caregiver(spc_dict=spc_dict, map_graph=map_graph, source_node=copy_me.current_location)
            if destination_to_remove[2] == 'p':

                added_time = datetime.timedelta(seconds=spc_dict[copy_me.current_location][1][destination_to_remove[1].origin])
                self.current_location = destination_to_remove[1].origin
                self.time = copy_me.time + added_time

            else:
                added_time = spc_dict[copy_me.current_location][1][destination_to_remove[1].destination]
                self.time = copy_me.time + added_time
                self.current_location = destination_to_remove[1].destination

                #The time added to the accumulated dealy will be -
                # The time we got to it's dest (self.time) - the earilest time the person could have gotten to his\her dest, by driving alone (i.e. the delay he suffered by using our service - how much time was added to his journey because he used our service, and not driving alone at the time he requested)
                self.accumulating_delay += self.time - destination_to_remove[1].earliest_time_to_dest

            #set this node's vehicle to be the same as that of the node you are copying from
            #copy the current_possible_destinations as well, from the previous node, and remove the destination you just drove to

            # self.my_vehicle = copy_me.my_vehicle #Not using vehicle anywhere, so not copying it
            self.current_possible_destinations = copy.copy(copy_me.current_possible_destinations) #Don't think a deep copy is needed here. Items in current_possible_destinations are tuples, of time left (int, will be copied without problem, doesn't need deep copy),
            # , the request (OK to point to. Only thing that can change in it is the estimated_dropoff_time, and that doesn't matter here), and a char that indicates whether this is a pickup or dropoff, and that shouldn't change either.
            self.current_possible_destinations.remove(destination_to_remove) #TODO - make sure this works, that the relevant tuple is removed from the current_possible_destinations

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
                    c[0] = c[0] + spc_dict[self.previous_location][c[1].origin] - added_time - spc_dict[self.current_location][c[1].origin]
                else:
                    c[0] = c[0] + spc_dict[self.previous_location][c[1].destination] - added_time - spc_dict[self.current_location][c[1].destination]
                # c[0] = c[1]. self.time + spc_dict

            if destination_to_remove[2] == 'p':  # if the vehicle drove to a request, a pickup, add the drop-off to the current_possible_destinations
                #calculte the extra_time_left_to_drop-off, by taking the request's estimated_dropoff_time, subtract the "current" time (self.time, the time this vehicle would reach this current location) and subtract the time to drive
                # from current_location to the destination of the ndoe we picked up
                extra_time_left_to_dropoff = destination_to_remove[1].estimated_dropoff_time - self.time - spc_dict[self.current_location][destination_to_remove[0].destination]

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
                self.current_possible_destinations.append((extra_time_left_to_dropoff, vr, 'd')) #the 'd' is to say this is a drop-off

            self.current_possible_destinations.sort(key=operator.itemgetter(0))
