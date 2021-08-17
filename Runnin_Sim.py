import Trip
import Vehicle
import Runnin_Sim
import Request
import Sim_init
import osmnx as ox


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

