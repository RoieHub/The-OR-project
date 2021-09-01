import Request
import networkx as nx
import datetime as dt


# Private case two requests (Mainly for RV graph)


#This function returns boolean of the "virtual trip" of r1 and r2 are valid.
# This  function uses import datetime as dt exhaustive search ,  and can be improved
def valid_trip2_min_cost(r1, r2, map):
    # Check both trips Z constraints

    # First we make sure that the first and most important condition is true
    # That is - if a virtual taxi, starting from r1 drives to r2, will it get
    # there in time? (i.e. - before r2.latest_time_to_pick_up)

    # Cacl travel times and time of arrival driving from r1 to r2
    # nx.algorithms.shortest_paths.generic.shortest_path_length
    r1S_to_r2S_pathDuration = nx.shortest_path_length(map, r1.origin, r2.origin, weight='travel_time')# d
    time_of_arrival_to_r2 = dt.datetime.now() + dt.timedelta(seconds=r1S_to_r2S_pathDuration)

    #in case we can't reach r2.origin in time
    if time_of_arrival_to_r2 > r2.latest_time_to_pick_up:
        return False, -1

    #now we need to check that a permutation exists where -
    # 1 - r2 doesn't wait until after his latest_time_to_pick_up
    # 2 - both r1 and r2 reach their respective destinations without

    #first we calculate all 6 possible steps in path.
    r1S_to_r1D_pathDuration = nx.shortest_path_length(map, r1.origin, r1.dest, weight='travel_time')# a

    r2S_to_r2D_pathDuration = nx.shortest_path_length(map, r2.origin, r2.dest, weight='travel_time')#c
    r2S_to_r1D_pathDuration = nx.shortest_path_length(map, r2.origin, r1.dest, weight='travel_time')#b

    #r1D_to_r2S_pathDuration = nx.shortest_path_length(map, r1.dest, r2.origin, weight='travel_time')#b
    r1D_to_r2D_pathDuration = nx.shortest_path_length(map, r1.dest, r2.origin, weight='travel_time')#e

    #r2D_to_r1D_pathDuration = nx.shortest_path_length(map, r2.dest, r1.dest, weight='travel_time')# e

    r2D_to_r1S_pathDuration = nx.shortest_path_length(map, r2.dest, r1.origin, weight='travel_time') # f

    # Ver 1 exhaustive search

    # r1 r1 r2 r2
    p1 = r1S_to_r1D_pathDuration + r2S_to_r1D_pathDuration + r2S_to_r2D_pathDuration
    # r1 r2 r1 r2
    p2 = r1S_to_r2S_pathDuration + r2S_to_r1D_pathDuration + r1D_to_r2D_pathDuration
    # r1 r2 r2 r1
    p3 = r1S_to_r2S_pathDuration + r2S_to_r2D_pathDuration + r1D_to_r2D_pathDuration
    # r2 r2 r1 r1
    p4 = r2S_to_r2D_pathDuration + r2D_to_r1S_pathDuration + r1S_to_r1D_pathDuration
    # r2 r1 r2 r1
    p5 = r1S_to_r2S_pathDuration + r2D_to_r1S_pathDuration + r1D_to_r2D_pathDuration
    # r2 r1 r1 r2
    p6 = r1S_to_r2S_pathDuration + r1S_to_r1D_pathDuration + r1D_to_r2D_pathDuration

    #shortest if only care of cost
    best_path = min(p1,p2,p3 ,p4,p5 , p6)

