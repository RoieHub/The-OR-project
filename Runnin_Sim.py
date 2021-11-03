import copy
import datetime

import networkx
import networkx as nx
import Greedy_assignment
import spc_dict_caregiver
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
def init_ny_vehicles(num_of_vehicles,current_time):
    # Open a log for the run.
    #logging.basicConfig(level=logging.INFO,filename='or_'+str(datetime.datetime.now()).replace(':', '_')+'.log')
    # Basic useage example :  logging.INFO('This will be logged)
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    v_start_ids = [42446021, 42442463, 3099327950, 42440022, 42430263, 42434340]
    v_list = []
    for i in range(0, num_of_vehicles):
        v = Vehicle.Vehicle(v_start_ids[i % (len(v_start_ids))],time=current_time)
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
    list_of_rows = list_of_csv_rows(requests_csv_path)
    epochs_list = []
    epoch = []
    e_len = datetime.timedelta(seconds=epoch_len_sec)
    start = (str_to_time(list_of_rows[1][1]))
    if starting_time is not None:
        start = str_to_time(starting_time) #+e_len Ofir - I commented this out as I think this is a mistake.
    ending = start + datetime.timedelta(seconds=(epoch_len_sec*num_of_epochs))
    curr_epoch_starting_time = start
    curr_epoch_ending_time = start + e_len
    for r in list_of_rows:
        request_time = str_to_time(r[1])
        if r[0] == '1666870':
            print('1666870 is here')
        if request_time < curr_epoch_starting_time: # This request is before our epoch.
            continue
        elif request_time >= curr_epoch_starting_time and request_time < curr_epoch_ending_time and request_time < ending: # This is in our current epoch
            # Request quality check.
            if not check_node_in_graph(int(r[2]), map_graph):
                print("Skipping request with id = " + str(int(r[0])) + ", because origin not in graph. Origin = " + str(
                    int(r[2])) + ".")
                continue
            if not check_node_in_graph(int(r[3]), map_graph):
                print("Skipping request with id = " + str(int(r[0])) + ", because dest not in graph. Origin = " + str(
                    int(r[3])) + ".")
                continue
            # Append the current request to this epoch.
            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=request_time, spc_dict=spc_dict, map_graph=map_graph, data_line_id=int(r[0])))

            # Ofir - Check if the new request's self.earliest_time_to_dest == self.time_of_request.
            # That is a sign we should ignore the request (because shortest path between origin and dest couldn't be found)

            if epoch[-1].earliest_time_to_dest == epoch[-1].time_of_request:
                print("Dropping the request, because earliest_time_to_dest == time_of_request ")
                epoch.pop()
            continue
        elif request_time >= curr_epoch_ending_time and request_time < ending: # This is a request for a new epoch to be created.
            # Append the epoch to epoch_list
            epochs_list.append(copy.copy(epoch))
            # Clear the epoch
            epoch.clear()
            # Update epoch boundries
            curr_epoch_starting_time += e_len
            curr_epoch_ending_time+=e_len

            # This code's purpose - check above comment, in previous elif
            if not check_node_in_graph(int(r[2]), map_graph):
                print("Skipping request with id = " + str(int(r[0])) + ", because origin not in graph. Origin = " + str(
                    int(r[2])) + ".")
                continue
            if not check_node_in_graph(int(r[3]), map_graph):
                print("Skipping request with id = " + str(int(r[0])) + ", because dest not in graph. Origin = " + str(
                    int(r[3])) + ".")
                continue

            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=request_time, spc_dict=spc_dict,
                                         map_graph=map_graph, data_line_id=int(r[0])))

            # This code's purpose - check above comment, in previous elif
            if epoch[-1].earliest_time_to_dest == epoch[-1].time_of_request:
                print("Dropping the request, because earliest_time_to_dest == time_of_request ")
                epoch.pop()

            continue
        elif request_time >= ending:
            if epoch:  # If epoch not empty , append it to epoch_list .
                epochs_list.append(copy.copy(epoch))
                epoch.clear()
            break
        else:
            raise Exception("Sorry, problem with line " + str(r))
    if epoch:  # If epoch not empty , append it to epoch_list .
        epochs_list.append(copy.copy(epoch))
        epoch.clear()
    return epochs_list









def check_node_in_graph(node_number: int, map_graph: networkx.Graph):
    if node_number in map_graph.nodes:
        return True
    else:
        return False

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

"""
This function used in the end of epoch ,to check if the vehicle v is assinged a new trip by greedy algo.

"""
#def is_assinged_new_trip(v,assinged_tv):
def update_v_location(v, path, curr_time, epoch_len, spc_dict, map_graph):
    # PAT^H IS (r_i,p/d)
    # Find location
    # time_spent is a time accumulator that we already spent traveling on the path.
    time_spent = datetime.timedelta(seconds=0)
    # Iterating over each stop in the v path.
    # as long as we can reach the next stop within our time limit (epoch length) , we 'go' to the next stop , updating current position
    for next_stop_tuple in path:
        next_stop_id = 0
        pickup = False
        # This if updates 'next_stop_id' , if its 'p' its the pickup node of request , else its the dropoff node of request.
        if next_stop_tuple[1] == 'p': # This is the pickup node
            next_stop_id = next_stop_tuple[0].origin
            pickup = True
        else:
            next_stop_id = next_stop_tuple[0].destination
            pickup = False
        time_to_next_stop = datetime.timedelta(seconds=spc_dict[v.curr_pos][1][next_stop_id])
        if time_to_next_stop <= (epoch_len - time_spent): # If we get to this stop within our epoch time limit.
            v.curr_pos = next_stop_id # update v current possiotion as the next stop.
            time_spent += time_to_next_stop # accumulate the time spent going until here.
            if pickup:
                v.add_passengers(next_stop_tuple[0])
                next_stop_tuple[0].update_actual_pick_up_time(curr_time+time_spent)

        else:
            # "path_to_last_stop" is the path to the next stop on the path given to the function, and we can't reach that stop before the time limit (the next epoch ends)
            path_to_last_stop = copy.copy(spc_dict[v.curr_pos][0][next_stop_id]) #copy so we don't change spc_dict
            path_to_last_stop.pop(0) #pop the first because that paths in spc_dict always start with the origin node

            # Instead of using spc_dict here, we can use the travel_time value that exists between each neighboring nodes.
            # That value already exists, as we always first run "add_edge_speeds()" and "add_edge_travel_times()" at the beginning of the simulation.
            # This way we save the time spc_dict_caregiver would spend calculating the paths and times from v.curr_pos to all of the graph.
            time_to_next_middle_stop = map_graph[v.curr_pos][path_to_last_stop[0]][0]['travel_time']

            while time_spent + time_to_next_middle_stop <= epoch_len:
                v.curr_pos = path_to_last_stop.pop(0)
                time_spent += time_to_next_middle_stop

                time_to_next_middle_stop = map_graph[v.curr_pos][path_to_last_stop[0]][0]['travel_time']


            break #TODO: make sure this breaks the above for loop






def update_v_after_e(v_list, v_ok: set, assigned_tv: list, curr_time, epoch_len, spc_dict, map_graph):
   # First we create a set of vehicles with no new trips assigned.
   v_set = set(v_list)
   v_nok = v_set-v_ok
   # Update the location of vehicles with no new assignments.
   for v in v_nok:
        if v.passengers :# This checks if current passengers list is empty https://flexiple.com/check-if-list-is-empty-python/
            print('idle vehicle' + str(v)) # TODO something with idel.
        # TODO: else:

   # Update the location of vehicles with new assignments.
   for assi in assigned_tv:
       v = assi[1]
       path = assi[3]
       update_v_location(v, path, curr_time, epoch_len, spc_dict, map_graph)



       # UPdate the location somehow


   #def __init__(self, requests_list: Tuple[Request.Request, ...], vehicle_list: Tuple[Vehicle.Vehicle, ...], virtual_vehicle: Vehicle, map_graph: nx.Graph, current_time: datetime ,spc_dic


def running_ny_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    curr_time = str_to_time(starting_time)
    # Virtual vehicle for algorithm purpose.
    virtual_v = Vehicle.Vehicle(0,curr_time)

    v_list = init_ny_vehicles(num_of_vehicles,current_time=curr_time)


    # Creating Shortest paths costs dictionary to hold those val's.
    #global spc_dict
    spc_dict = {}

    # Creating our map_graph.
    map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    #G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    map_graph = ox.add_edge_speeds(map_graph)
    map_graph = ox.add_edge_travel_times(map_graph)
    # Create logger.
    # logging.basicConfig(filename=str(datetime.datetime.now())+'.log',level=logging.INFO)
    logging.basicConfig(filename=str(datetime.datetime.now()).replace(':', '_')+'.log', level=logging.INFO) #Difference from above line makes it work on Windows - can't use ':' in filename in windows

    # Example :logging.info('This will get logged to a file')

    #Stats for log
    rate_of_epoch_sucsess = 0
    rate_of_run_sucsess = 0
    logging.info('This run : ST= : '+ starting_time +', epoch_len = '+ str(epoch_len_sec) +' , num of epochs = '+ str(num_of_epochs) + ", num of vehicles = "+ str(num_of_vehicles) +'\n')
# def running_ny_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    epochs = epoch_separator(requests_csv_path=csv_path, epoch_len_sec=epoch_len_sec, num_of_epochs=num_of_epochs, starting_time=starting_time,spc_dict=spc_dict, map_graph=map_graph )
    added_time = datetime.timedelta(seconds=epoch_len_sec)
    # Working on each Epoch
    for count,epoch in enumerate(epochs):
        curr_time += added_time
        rv = RV_graph.RV_graph(requests_list=epoch, vehicle_list=v_list, virtual_vehicle=virtual_v, map_graph=map_graph, current_time=curr_time, spc_dict=spc_dict)
        rtv = RTV_graph.RTV_graph(rv_graph=rv, spc_dict=spc_dict, map_graph=map_graph, current_time=curr_time) # TODO Check if current time needed as well
        greedy = Greedy_assignment.Greedy_assingment(rtv)
        # TODO : here we need to assigning trips to vehicles
        epoch_set = set(epoch)
        r_nok = epoch_set-greedy.r_ok # This is set difference , so only unserved requests are here.

        # Update log of this epoch
        logging.info(
            'E' + str(count) + ' : ' + str(epoch[0].time_of_request) + ' to ' + str(epoch[-1].time_of_request) + '\n')
        # Update rate of sucsess
        rate_of_epoch_sucsess = len(greedy.r_ok) / len(epoch)  # The number of sent requests this epoch

        logging.info('Epoch sucsess rate' +str(rate_of_epoch_sucsess*100)+'%'+'\n')

        if len(r_nok) != 0 and (len(epochs) -1) != count :# If no r to append and this is not the last epoch.
            epochs[count+1] = list(r_nok) + epochs[count+1] #TODO check validity

        #Update all vehicles with
        update_v_after_e(v_list, greedy.v_ok, greedy.assigned_tv, curr_time, added_time, spc_dict, map_graph)
        # update_penalties(r_nok) # TODO what to update?

        #Update log of this epoch

        #logging.info()
        # What to do with all the data?

        # Last operation in each epoch.
        for v in v_list:
            v.clear_rv_after_epoch()
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
    # print('this is main, now lets see...')
    # start_time=datetime.datetime.now()
    running_ny_sim('requests.csv', 10, 1, 30, starting_time='2013-05-05 00:00:01')
    # print('====== is took : '+str(datetime.datetime.now() - start_time))






