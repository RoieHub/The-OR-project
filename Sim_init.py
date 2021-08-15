
# This class hold Several parameters to init a simulation
import osmnx as ox
import datetime

class Sim_init:
    #Vehicle stats
    fleet_size : int # Fixed fleet size for simulation.
    v_cap : int # Vehicle capacity , maximun num of passengers.
    #Times
    #datetime.timedelta documentation :A duration expressing the difference between two date, time, or datetime instances to microsecond resolution.
    max_delay : datetime.timedelta # The difference between the drop off time and minimal time to reach destination.==: delta = Request.toed - Requst.toe
    #map : dafaultivly 'Raanana, Israel'

    # This is default constructor in raanana city
    def __init__(self):
        self.fleet_size = 1
        self.v_cap = 10
        self.max_delay = datetime.timedelta(minutes=10)
        self.map = ox.graph_from_place('Raanana, Israel', network_type='drive')

