
# This class hold Several parameters to init a simulation
import osmnx as ox
import datetime
import pandas as pd

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
        #Init the map
        self.map = ox.graph_from_place('Raanana, Israel', network_type='drive')
        #Add speeds and time travel to map
        self.map = ox.add_edge_speeds(self.map)
        self.map = ox.add_edge_travel_times(self.map)

    def __init__(self,trips_csv ):

        self.fleet_size = 1
        self.v_cap = 10
        self.max_delay = datetime.timedelta(minutes=10)
        # Init the map
        self.map = ox.graph_from_place('Raanana, Israel', network_type='drive')
        # Add speeds and time travel to map
        self.map = ox.add_edge_speeds(self.map)
        self.map = ox.add_edge_travel_times(self.map)


    """
    CSV file must be sorted by timeStamp
    """
    def extract_requests_from_csv(self,csv_file_path ,map_name , epoch_len_sec):

        # I fucking Hate pandas time stamps, they are shit
        requestList = []
        df1 = pd.read_csv('nyc2015_clean_sim.csv')
        starting_time = df1['tpep_pickup_datetime'][0]
        epoch = []
        i = 0
        #for time in d
        return requestList


