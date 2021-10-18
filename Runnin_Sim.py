import copy
import datetime
from roies_util import str_to_time
import Trip
import Vehicle
import Runnin_Sim
import Request
import Sim_init
import osmnx as ox
import RV_graph
import RTV_graph
import Epoch
from csv import reader
import Vehicle

"""
This functions creates a list of vehicles to be used in the sim.
Param:
@ num_of_vehicles : Natural number,"evenly" distribute vehicles between 6 starting points in "Manhattan NYC".
Return:
@ v_list : list of new vehicles
"""
def init_ny_vihecles(num_of_vehicles ) :
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    v_start_ids = [42446021, 42442463, 3099327950, 42440022, 42430263, 42434340]
    v_list = []
    for i in range(0, num_of_vehicles):
        v = Vehicle.Vehicle(v_start_ids[i % (len(v_start_ids))])
        #v = Vehicle.Vehicle(422)
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
def epoch_separator(requests_csv_path , epoch_len_sec , num_of_epochs , starting_time = None):
    # Pull the request from csv as dataframe.
    list_of_rows = list_of_csv_rows(requests_csv_path)
    epochs_list = []
    epoch = []
    current_time = str_to_time(list_of_rows[1][1])
    if starting_time is not None:
        current_time = starting_time
    ending_time = current_time + datetime.timedelta(seconds=(epoch_len_sec*num_of_epochs))
    e_len = datetime.timedelta(seconds=epoch_len_sec)
    for r in list_of_rows:
        if r[1] == 'pickup_datetime':
            continue
        pu_time = str_to_time(r[1])
        if pu_time < current_time: # Not in our Epochs.
            continue
        elif pu_time < (current_time+e_len): # Request is in current epoch
            epoch.append(Request.Request(r[2],r[3],pu_time))
            continue
        elif pu_time >= (current_time+e_len) and (current_time+e_len) <= ending_time: # This belong to a new epoch.
            # Append the epoch to epoch_list
            epochs_list.append(copy.copy(epoch))
            # Clear the epoch
            epoch.clear()
            #Update current time
            current_time += e_len
            epoch.append(Request.Request(r[2], r[3], pu_time))
            continue
        elif pu_time >= ending_time:
            break
        else :
            raise Exception("Sorry, problem with line " + str(r))
    return epochs_list

















def list_of_csv_rows(requests_csv_path):
        csv_file = open(requests_csv_path, 'r')
        csv_reader = reader(csv_file)
        # Passing the cav_reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        csv_file.close()
        return list_of_rows














def running_sim_full_ny(epoch_list, num_of_vehicles):

    v_list = init_ny_vihecles(num_of_vehicles)

    # Working on each Epoch
    for epoch in epoch_list:
        RV =  RV_graph(epoch , v_list)
        RTV = RTV_graph(RV)




def run_sim1():


    sim1 = Sim_init()
    map = sim1.map

    pellersHouse = ox.distance.nearest_nodes(map, 32.17939774515874, 34.8552841962678)
    print(pellersHouse)
    return

