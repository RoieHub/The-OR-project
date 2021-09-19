import Trip
import Vehicle
import Runnin_Sim
import Request
import Sim_init
import osmnx as ox
import RV_graph
import RTV_graph

def running_sim_full_ny(epoch_list, num_of_vehicles):
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    v_start_ids = [42446021,42442463,3099327950,42440022,42430263,42434340]
    v_list = []
    for i in range(1,num_of_vehicles):
        v = Vehicle(v_start_ids[i % len(v_start_ids)])
        v_list.append(v)

    # Working on each Epoch
    for epoch in epoch_list:
        RV =  RV_graph(epoch , v_list)
        RTV = RTV_graph(RV)




def run_sim1():

    #   Sim Locations
    """Peller's House
32.17939774515874, 34.8552841962678


Arcaffe - jerusalem street
32.18551213559752, 34.854385078898844
Frsh Market
32.19108499229568, 34.86322054442748
Meatland
32.1814488139893, 34.87337296766117
Raanana City Hall
32.17981502832255, 34.87639411145554

bonus-unseen on map
Alon middle school
32.18618322812021, 34.864462996201055

"""
    sim1 = Sim_init()
    map = sim1.map

    pellersHouse = ox.distance.nearest_nodes(map, 32.17939774515874, 34.8552841962678)
    print(pellersHouse)
    return

