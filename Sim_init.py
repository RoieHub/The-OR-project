
# This class hold Several parameters to init a simulation
import osmnx as ox
from datetime import datetime
from datetime import timedelta
import pandas as pd
from roies_util import str_to_time
import Request





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
    :param 
    example epoch_len = timedelta(seconds=30) 
    :param map_name
    :returns A list of lists of requests , where each list is an epoch.
    """
    def extract_requests_from_csv(self,csv_file_path ,map_name , epoch_len):
        df = pd.read_csv('nyc2015_clean_sim.csv')
        epoch_list = []
        epochs = []
        epoch_start = str_to_time(df['tpep_pickup_datetime'][0])
        for index, row in df.iterrows():
            pu_time = str_to_time(row['tpep_pickup_datetime'])
            if pu_time <= (epoch_start + epoch_len): # Same Epoch
                # Create Request
                req = Request(row['src'],row['dst'],pu_time)
                epochs.append(req)

            else: # Next epoch
                epoch_start += epoch_len
                # End this epoch by append it to epoch list.
                epoch_list.append(epochs)
                epochs.clear() # clear epoch to collect the next epoch
                req = Request(row['src'], row['dst'], pu_time)
                epochs.append(req)


        return epoch_list




