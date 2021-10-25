import copy
import datetime

import networkx as nx

import Greedy_assignment
from roies_util import str_to_time
import Trip
import Vehicle
import Runnin_Sim
import Request
import Sim_init
import osmnx as ox
import RV_graph
import RTV_graph
from csv import reader
import Vehicle
import logging


"""
This functions creates a list of vehicles to be used in the sim.
Param:
@ num_of_vehicles : Natural number,"evenly" distribute vehicles between 6 starting points in "Manhattan NYC".
Return:
@ v_list : list of new vehicles
"""
def init_ny_vehicles(num_of_vehicles):
    # Open a log for the run.
    #logging.basicConfig(level=logging.INFO,filename='or_'+str(datetime.datetime.now()).replace(':', '_')+'.log')
    # Basic useage example :  logging.INFO('This will be logged)
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    v_start_ids = [42446021, 42442463, 3099327950, 42440022, 42430263, 42434340]
    v_list = []
    for i in range(0, num_of_vehicles):
        v = Vehicle.Vehicle(v_start_ids[i % (len(v_start_ids))])
        v_list.append(v)
    return v_list




"""
This method creates epochs of requests from a csv.
Param:
    @request_csv_path : A path to the csv file where request are stored.
    @epoch_len_sec : Positive integer , represent the length of an epoch in seconds.
    @num_of_epochs : Positive integer, the num of epochs needed.
    @starting_time : String , represents the time of the first request of the first epoch , tested format (but not exclusive) 'YYY-MM-DD hh:mm:ss' exmaple of may the first'2013-05-01 00:00:01'
    
:returns : List of lists of requests. where list[i] is the list of the ith epoch , where all requests are between [starting time + (epoch_len_sec * i ),starting time + (epoch_len_sec * (i+1) )]

"""
def epoch_separator(requests_csv_path , epoch_len_sec , num_of_epochs ,spc_dict , map_graph, starting_time = None ):
    # Pull the request from csv as dataframe.
    list_of_rows = list_of_csv_rows(requests_csv_path)
    epochs_list = []
    epoch = []
    e_len = datetime.timedelta(seconds=epoch_len_sec)
    current_time = str_to_time(list_of_rows[1][1]) # TODO Check if + e_len needed here.
    if starting_time is not None:
        current_time = str_to_time(starting_time)+e_len
    ending_time = current_time + datetime.timedelta(seconds=(epoch_len_sec*num_of_epochs))

    for r in list_of_rows:
        if r[1] == 'pickup_datetime':
            continue
        pu_time = str_to_time(r[1])
        if pu_time < current_time: # Not in our Epochs.
            continue
        elif pu_time < (current_time+e_len): # Request is in current epoch
            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=pu_time, spc_dict=spc_dict, map_graph=map_graph,data_line_id=int(r[0])))
            continue
        elif pu_time >= (current_time+e_len) and (current_time+e_len) <= ending_time: # This belong to a new epoch.
            # Append the epoch to epoch_list
            epochs_list.append(copy.copy(epoch))
            # Clear the epoch
            epoch.clear()
            #Update current time
            current_time += e_len
            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=pu_time, spc_dict=spc_dict, map_graph=map_graph,data_line_id=int(r[0])))
            continue
        elif pu_time >= ending_time:
            break
        else :
            raise Exception("Sorry, problem with line " + str(r))
    return epochs_list

"""
This function reads a file of "requests and returnes a list of rows from the csv"
:param :request_csv_path , the path to the csv file on your system. 
"""
def list_of_csv_rows(requests_csv_path):
        csv_file = open(requests_csv_path, 'r')
        csv_reader = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        csv_file.close()
        return list_of_rows


def running_ny_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    # Virtual vehicle for algorithm purpose.
    virtual_v = Vehicle.Vehicle(0)

    v_list = init_ny_vehicles(num_of_vehicles)


    # Creating Shortest paths costs dictionary to hold those val's.
    #global spc_dict
    spc_dict = {}

    # Creating our map_graph.
    map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    #G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    map_graph = ox.add_edge_speeds(map_graph)
    map_graph = ox.add_edge_travel_times(map_graph)
    # Create logger.
    logging.basicConfig(filename='app.log',level=logging.INFO)
    # Example :logging.info('This will get logged to a file')

    epochs = epoch_separator(requests_csv_path=csv_path, epoch_len_sec=epoch_len_sec, num_of_epochs=num_of_epochs, starting_time=starting_time,spc_dict=spc_dict, map_graph=map_graph )

    curr_time = str_to_time(starting_time)
    added_time = datetime.timedelta(seconds=epoch_len_sec)
    # Working on each Epoch
    for epoch in epochs:
        curr_time += added_time
        rv = RV_graph.RV_graph(requests_list=epoch, vehicle_list=v_list, virtual_vehicle=virtual_v, map_graph=map_graph, current_time=curr_time, spc_dict=spc_dict)
        rtv = RTV_graph.RTV_graph(rv_graph=rv, spc_dict=spc_dict, map_graph=map_graph, current_time=curr_time) # TODO Check if current time needed as well
        greedy = Greedy_assignment.Greedy_assingment(rtv)
        print('It is alive!')




"""
This are function for testing area
"""

def init_simple_vehicles(num_of_vehicles):
    # Open a log for the run.
    #logging.basicConfig(level=logging.INFO,filename='or_'+str(datetime.datetime.now()).replace(':', '_')+'.log')
    # Basic useage example :  logging.INFO('This will be logged)
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    v_start_ids = [0, 4, 20, 24]
    v_list = []
    for i in range(0, num_of_vehicles):
        v = Vehicle.Vehicle(v_start_ids[i % (len(v_start_ids))])
        v_list.append(v)
    return v_list

def create_simple_graph(id):
    map_graph = nx.Graph()
    if id == 1:
        # Creating width edges weighted 1.
        for row in range(5):
            for i in range(5*row,(5*row)+4):
                map_graph.add_edge(i, (i + 1), travel_times=1)

        for row in range(4):
            for i in range(5*row,(5*row)+4):
                map_graph.add_edge(i, (i + 5), travel_times=1)
    return map_graph



def Running_simple_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    # Virtual vehicle for algorithm purpose.
    virtual_v = Vehicle.Vehicle(0)

    v_list = init_simple_vehicles(num_of_vehicles)

    # Creating Shortest paths costs dictionary to hold those val's.
    # global spc_dict
    spc_dict_simple = {}

    # Creating our map_graph.
    map_graph = create_simple_graph(id=id)

    # Create logger.
    logging.basicConfig(filename='app.log', level=logging.INFO)
    # Example :logging.info('This will get logged to a file')

    epochs = epoch_separator(requests_csv_path=csv_path, epoch_len_sec=epoch_len_sec, num_of_epochs=num_of_epochs,
                             starting_time=starting_time, spc_dict=spc_dict_simple, map_graph=map_graph)

    curr_time = str_to_time(starting_time)
    added_time = datetime.timedelta(seconds=epoch_len_sec)
    # Working on each Epoch
    for epoch in epochs:
        curr_time += added_time
        rv = RV_graph.RV_graph(requests_list=epoch, vehicle_list=v_list, virtual_vehicle=virtual_v, map_graph=map_graph,
                               current_time=curr_time, spc_dict=spc_dict_simple)
        rtv = RTV_graph.RTV_graph(rv_graph=rv, spc_dict=spc_dict_simple, map_graph=map_graph,
                                  current_time=curr_time)  # TODO Check if current time needed as well
        greedy = Greedy_assignment.Greedy_assingment(rtv)
        print('It is alive!')


if __name__ == '__main__':
    print('this is main, now lets see...')
    start_time=datetime.datetime.now()
    running_ny_sim('clean_2013.csv',10, 1, 30, starting_time='2013-05-05 00:00:00')
    print('====== is took : '+str(datetime.datetime.now() - start_time))






