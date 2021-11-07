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
    # logging.basicConfig(level=logging.INFO,filename='or_'+str(datetime.datetime.now()).replace(':', '_')+'.log')
    # Basic useage example :  logging.INFO('This will be logged)
    # Generate  vehicles at starting nodes , chosen by Roie , based on Connor's work.
    # v_start_ids = [42446021, 42442463, 3099327950, 42440022, 42430263, 42434340]
    v_start_ids = [42435642, 42439440, 42423051, 4461990857, 42435660, 42435657, 42443804, 4443775465, 370892861, 42435422, 42437654, 42446959, 42435663, 4557517555, 42429334, 3786876206, 42430271, 42435644, 42446971, 42430371, 42430367, 42428007, 42430384, 42430265, 42435596, 42445039, 3639382769, 42430295, 42444909, 42430375, 1331391393, 42437914, 42430394, 42429659, 42429412, 42447020, 42437881, 6177439759, 42432818, 5849918504, 42430253, 42428297, 42430277, 42440022, 42427762, 42430342, 42430378, 42449945, 42435675, 42443680, 42423674, 42439842, 42435684, 42440743, 42435671, 42429338, 42447009, 42438889, 42437890, 42439286, 42435680, 42431544, 42436710, 42431549, 42428303, 42439984, 42439389, 42430304, 42440009, 42446849, 42445378, 42429340, 42439990, 42440729, 42422026, 42430333, 42436486, 42443336, 42435654, 42442247, 42440020, 42435714, 42438547, 42440459, 42440951, 42446991, 42445417, 42430274, 42445018, 42440153, 42445947, 42436492, 42430356, 5706568771, 2298803471, 42436707, 42443388, 42443975, 42436700, 42432847, 4557517554, 42440721, 42430298, 42435420, 42436439, 42446013, 42432589, 42440012, 278608643, 42443027, 42439823, 42430358, 42446701, 42440015, 42435677, 42430597, 42437371, 42436159, 42432700, 42429374, 42427915, 42446987, 42430344, 42436705, 42456060, 3799572065, 42433620, 42430263, 42430187, 42430259, 42434821, 42427483, 42443807, 42455643, 42438784, 42440710, 42430338, 42443556, 42450426, 42448701, 42440465, 42446353, 247084442, 5145323793, 42432580, 42430673, 42442957, 42432861, 42445498, 42440452, 42445037, 42442952, 42449928, 42437909, 371188756, 42430292, 42427371, 42427423, 42435702, 42449956, 42429976, 42437644, 42439840, 42437368, 42445310, 42430363, 42438891, 42445534, 42442955, 4347534767, 42427764, 42421889, 42437021, 42431556, 42447007, 42442959, 42430361, 42439981, 42445661, 5131026388, 588455698, 42428305, 4557517552, 42442432, 42428493, 42430269, 42430352, 42442937, 42445390, 42440004, 42437363, 42435716, 42430217, 42430308, 42428003, 8122411159, 6223969260, 42446998, 42434871, 42440001, 42444051, 42445027, 42445916, 42446933, 42430231, 42432585, 42445953, 42439272, 42437358, 42436941, 42436753, 42434807, 1773084402, 42443353, 42435599, 42438894, 42436746, 42446994, 42430235, 42427426, 4597668043, 1061531685, 42422270, 42446016, 42430279, 4288677093, 42439006, 42432825, 42427805, 42449886, 42428005, 42435275, 42432060, 42436531, 42428170, 42436489, 42428020, 42437084, 42429657, 7490266268, 42444991, 42427991, 42449341, 42439001, 42430347, 42445888, 42430241, 42446021, 42449947, 42446977, 42449991, 42434800, 7106818626, 42452026, 42431165, 42440463, 42428588, 42450015, 42430063, 42442943, 42443313, 42436511, 42442960, 4347534783, 42445656, 42445236, 42454378, 42449961, 42430320, 42435598, 42446275, 4597668028, 42435624, 3718672443, 42439952, 42439996, 42442948, 42430350, 42436519, 42452973, 42442889, 42434072, 42430237, 42428037, 42428444, 42430282, 42430694, 42443528, 42454325, 42435687, 42430249, 42448379, 42435645, 42454433, 42449942, 2711029280, 42443950, 42439972, 42430154, 42430390, 42428579, 42445413, 42424225, 42445011, 42448390, 42428328, 42443561, 42431490, 42448707, 4443775464, 42427369, 42446986, 1773084405, 42446466, 1061531447, 42428570, 42437663, 42443403, 42449918, 42428634, 42442857, 42429324, 42445374, 370880758, 42443671, 42427374, 42430745, 42447132, 42428321, 42445950, 42449954, 42443280, 42442480, 42444049, 42440163, 42431154, 42438961, 42430288, 42439323, 42454428, 42436484, 42430324, 42439994, 42430317, 596775882, 42429394, 42429661, 42432444, 42443024, 42432703, 42440737, 370924957, 42429342, 42439406, 42434090, 42430989, 42434205, 42445025, 42447105, 42428329, 42445649, 42423296, 42439236, 42428312, 42440934, 42439968, 42427786, 42430311, 42429980, 42452882, 42427327, 42435707, 42432693, 42453575, 42427797, 42430068, 42445917, 42439561, 42429876, 42431000, 42436396, 42442947, 42443614, 42429981, 42449948, 42434215, 42439955, 42453630, 42428491, 42435646, 4557495130, 42430075, 42429986, 42431654, 42442933, 42432451, 42439836, 42436939, 42447149, 4597668041, 42445924, 42435650, 42443020, 42449333, 42436056, 42434959, 42427787, 42438859, 42428307, 42436477, 42432438, 42453902, 1241742627, 42435705, 42428014, 42445247, 42442961, 42439275, 42447237, 42437289, 42428447, 42434087, 42431678, 42440025, 42439834, 4862610026, 42428441, 42434946, 42445899, 42438800, 42435516, 4597668040, 42430811, 42428308, 42445936, 42448811, 1061531429, 42431656, 42436475, 4597668038, 42436714, 42445766, 62915549, 42436516, 42449314, 42448813, 42449021, 42430255, 42428287, 42447166, 42435603, 42446932, 42447136, 42452353, 42430041, 42433604, 42434140, 42430205, 42443811, 42448693, 42449938, 42431661, 42427477, 42440960, 42449985, 42431680, 42443029, 42429896, 1815133244, 42440326, 42428598, 42450820, 42429373, 42436510, 42438544, 42430257, 42428590, 42429773, 42446949, 42439964, 42434268, 42428315, 373880031, 596775900, 42430247, 42436586, 42449971, 42430688, 42442949, 42430903, 42439563, 42444985, 2298803428, 42442906, 42446472, 42437451, 42449963, 6173564360, 42443037, 42451674, 596775935, 42428010, 42438805, 42446533, 42455675, 42449926, 42443050, 42434270, 42436943, 42447030, 42448203, 42429664, 42430589, 42436701, 42428313, 42450028, 42445928, 42431508, 42443381, 42445885, 42436748, 42442286, 42440453, 42455963, 42439567, 42432594, 42428595, 42445930, 42446528, 42430118, 42442939, 42440397, 6177439752, 42428223, 100522728, 42435710, 42446488, 42453187, 4597668026, 42429769, 1825841742, 42430314, 42449576, 42431004, 42446942, 4321748237, 42439559, 42442913, 42445896, 42445020, 42443532, 42428643, 42431452, 42442935, 42437436, 42445033, 4347550074, 42446875, 42433611, 42436703, 596775867, 42421877, 42430329, 42437283, 42440469, 1692433916, 42431560, 42442459, 1692433932, 42429375, 42428015, 4597668032, 42439403, 42435578, 42456543, 42429562, 42437949, 42439181, 42428782, 42432068, 42428473, 42430983, 42438506, 42436336, 42437280, 42442931, 1061531787, 1692433928, 7480301866, 387180916, 42436537, 42442895, 42450030, 42450434, 42443618, 42432834, 42446270, 42442902, 1061531509, 42435514, 42434085, 42432706, 1061531634, 1773076509, 42445365, 42428022, 4138911201, 470209120, 1918039897, 42429874, 42455751, 42428489, 42439830, 42436921, 42430828, 390519635, 42429971, 42436913, 3786901743, 42454381, 42444829, 42430233, 42454010, 42429690, 42428216, 42439070, 42454701, 42444827, 42439170, 1061531491, 42435509, 42455761, 42434142, 42432464, 42443347, 6177439749, 42436944, 42432142, 5849918502, 42428601, 42442255, 42456049, 42431459, 42434271, 1061531603, 42445867, 42439203, 42438174, 42431470, 42450634, 42445910, 4597668036, 42445926, 42430164, 42437108, 42446086, 42428220, 4597668031, 42429662, 42443563, 42427390, 42421969, 42450009, 42453310, 596775946, 42445914, 5216470727, 42445909, 42436393, 42433625, 42438674, 42449982, 42430122, 42446363, 42430603, 42445001, 42446293, 42446935, 42430060, 42456598, 561042190, 42438503, 42429694, 1061531527, 42443326, 42456041, 42450025, 42439280, 596775919, 42436549, 42454423, 42445404, 42445976, 42446521, 42443344, 561042200, 42430052, 42449685, 42436355, 42432436, 42437384, 42436917, 42427812, 1241742563, 42426747, 42438886, 42436942, 42446945, 42443810, 42430803, 42438881, 42436381, 42446478, 42452951, 42427381, 42445520, 42452314, 42428029, 42449890, 42443264, 42439960, 42454994, 42445651, 42448238, 42438798, 42435610, 42443046, 596775907, 42443032, 6176483595, 42445941, 4597668030, 596775941, 42437339, 42443513, 42442276, 4491359481, 1825841704, 42428476, 42448257, 42435632, 42443042, 4597668029, 42430898, 42430736, 42452875, 1061531707, 42437096, 42430600, 42449893, 42434954, 42440270, 42442451, 42438802, 42445908, 42439826, 42436539, 42436919, 596775951, 42453601, 42439073, 42449017, 1919595915, 42445920, 42428016, 42440935, 42455695, 42431659, 42449308, 4597668039, 42435253, 42446547, 42428232, 42446925, 42428438, 42428027, 42440325, 42429974, 42448338, 42428674, 42456197, 42443048, 42445972, 42452365, 1773121034, 42443612, 596776177, 596776156, 42430886, 42445511, 596775985, 42428179, 42431168, 42427996, 7684225787, 42442898, 42446036, 42434439, 42431037, 42447144, 42434074, 42436754, 42446934, 42439416, 42445574, 42429330, 42453604, 6929267015, 42440323, 42443044, 42437343, 42428468, 42431681, 42428174, 596799866, 42445961, 42424439, 42427427, 42432214, 42430691, 42429314, 42442848, 596775998, 42434974, 42428310, 596776089, 596775930, 42444954, 42427324, 42447126, 1692433919, 42436404, 596776057, 42442862, 42442463, 42431684, 42434148, 42450044, 42432564, 42440350, 42436129, 596776260, 596776150, 42428332, 42428653, 42435522, 42437300, 42440170, 42428201, 42437670, 42429688, 42428013, 42438487, 42450341, 42442891, 42436788, 42454522, 42438862, 42443009, 42430550, 42436922, 42440829, 42448317, 42453952, 42438809, 6177439750, 42434352, 42432558, 42443928, 1773076778, 42446070, 42447084, 42456568, 42432066, 1773084410, 100522741, 42448563, 42448735, 42445903, 42445356, 6211334202, 42455867, 42421803, 42448745, 7802856341, 4320028826, 1692433938, 42456611, 42444814, 5706568625, 42437686, 42443346, 42442977, 42429663, 42436544, 42437401, 387184869, 5799117240, 42443268, 42430857, 42439556, 42448254, 42449067, 42434285, 42442850, 42443613, 42440330, 42435499, 42449597, 42431650, 42433565, 42442415, 42434948, 42442445, 1692433935, 42428640, 4597668020, 42437346, 42440456, 42428047, 42434279, 42435629, 42430742, 42430861, 42443349, 42432194, 42428192, 42436364, 42428714, 42449932, 42436751, 42431898, 42444964, 42443329, 42452956, 42431611, 6279091713, 42444817, 596776163, 4597668042, 42428790, 42442910, 42434196, 42436481, 42443534, 42428575, 42438509, 42428206, 42443341, 42438791, 42436590, 1061531807, 42439399, 42428368, 42430004, 42428024, 42447235, 42428034, 596775870, 42446941, 42443332, 42421996, 42422899, 42434175, 42447076, 42436014, 42428049, 42437425, 42453986, 42446889, 1773084407, 42428043, 42437951, 42427316, 42432856, 42449045, 42457476, 42436551, 42436335, 42444043, 42442534, 42428799, 42435272, 42428061, 42451787, 5812723035, 42428045, 42447115, 42459098, 1692433940, 42427386, 42442881, 42435633, 42428480, 561042188, 42436126, 42424089, 42454679, 42448558, 3786901738]
    v_list = []
    for i in range(0, num_of_vehicles):
        v = Vehicle.Vehicle(v_start_ids[i % (len(v_start_ids))], time=current_time)
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
        start = str_to_time(starting_time)  # +e_len Ofir - I commented this out as I think this is a mistake.
    ending = start + datetime.timedelta(seconds=(epoch_len_sec * num_of_epochs))
    curr_epoch_starting_time = start
    curr_epoch_ending_time = start + e_len
    for r in list_of_rows:
        request_time = str_to_time(r[1])
        if request_time < curr_epoch_starting_time: # This request is before our epoch.
            continue
        elif request_time >= curr_epoch_starting_time and request_time < curr_epoch_ending_time and request_time < ending: # This is in our current epoch

            # Request validity check.
            if not check_request_validity(int(r[0]), int(r[2]), int(r[3]), map_graph):
                continue
            # Append the current request to this epoch.
            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=request_time, spc_dict=spc_dict, map_graph=map_graph, data_line_id=int(r[0])))

            # Ofir - Check if the new request's self.earliest_time_to_dest == self.time_of_request.
            # That is a sign we should ignore the request (because shortest path between origin and dest couldn't be found)
            if epoch[-1].earliest_time_to_dest == epoch[-1].time_of_request:
                print("Dropping the request, because earliest_time_to_dest == time_of_request ")
                epoch.pop()

        elif request_time >= curr_epoch_ending_time and request_time < ending: # This is a request for a new epoch to be created.
            # Append the epoch to epoch_list
            epochs_list.append(copy.copy(epoch))
            # Clear the epoch
            epoch.clear()
            # Update epoch boundries
            curr_epoch_starting_time += e_len
            curr_epoch_ending_time += e_len

            if not check_request_validity(int(r[0]), int(r[2]), int(r[3]), map_graph):
                continue
            epoch.append(Request.Request(ori=int(r[2]), dest=int(r[3]), request_time=request_time, spc_dict=spc_dict,map_graph=map_graph, data_line_id=int(r[0])))

            # Ofir - Check if the new request's self.earliest_time_to_dest == self.time_of_request.
            # That is a sign we should ignore the request (because shortest path between origin and dest couldn't be found)
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

def check_request_validity(r_id:int, r_origin: int, r_dest:int, map_graph):
    if not check_node_in_graph(r_origin, map_graph):
        print("Skipping request with id = " + str(r_id) + ", because origin not in graph. Origin = " + str(r_origin) + ".")
        return False
    if not check_node_in_graph(r_dest, map_graph):
        print("Skipping request with id = " + str(r_id) + ", because dest not in graph. Origin = " + str(r_dest) + ".")
        return False
    # Check if the origin or dest of the request has not neighbors, i.e. after reaching the source\dest, we can't drive from it
    if (len(list(map_graph.neighbors(r_origin)))) == 0 or (len(list(map_graph.neighbors(r_dest)))) == 0:
        print("Dropping the request, because it's source or dest have no neighbors ")
        return False

    # This specific spot\node is problematic - you can drive FROM it, but not TO it.
    # There are better ways to do this, first thing that comes to mind is if a call to spc_dict gives an error, i.e. a node isn't reachable, remove that request. But that is something to be done at a later time. We need to finish the project.
    if r_origin == 5079840929 or r_dest == 5079840929:
        return False

    # OLD WAY of the next check - Ofir - Check if the new request's self.earliest_time_to_dest == self.time_of_request.
    # That is a sign we should ignore the request (because shortest path between origin and dest couldn't be found)
    if r_origin == r_dest:
        print("Dropping the request, because r_origin == r_dest ")
        return False

    #else:
    return True


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


"""
This function gets requests that weren't assigned in the last epoch, and filters out requests that their
latest_time_to_pickup will be expired (i.e. before the end of the last epoch)
"""
def filter_requests_time_to_pickup_over(r_nok, curr_time, added_time):
    remove_list = []
    for r in r_nok:
        if curr_time + added_time > r.latest_time_to_pick_up:
            remove_list.append(r)
    logging.info('num of Requests that cannot be served in the future :'+str(len(remove_list)))
    for r in remove_list:
        r_nok.remove(r)
    return r_nok # TODO: is this necessary?

def update_v_after_e(v_list, v_ok: set, assigned_tv: list, curr_time, epoch_len, spc_dict, map_graph):
    # First we create a set of vehicles with no new trips assigned.
    done_reqs = []
    v_set = set(v_list)
    v_nok = v_set - v_ok
    # Update the location of vehicles with no new assignments.
    idle_vehicles = []
    for v in v_nok:
        if not v.passengers:  # This checks if current passengers list is empty https://flexiple.com/check-if-list-is-empty-python/
            # We check this as if the passengers list is empty, the vehicle is idle (otherwise, even though it didn't get an assignment, there are people on it, meaning he has a trip to do.
            # print('idle vehicle' + str(v))  # TODO something with idle.
            idle_vehicles.append(v.id)
        else:  # else = vehicle v didn't get a trip assignment, and also has passengers on it.
            # We call "update_v_location" with the path being v.path, the path he has remaining from the last epoch.
            new_done_reqs = update_v_location(v, v.path, curr_time, epoch_len, spc_dict, map_graph)
            done_reqs.extend(new_done_reqs)
    print("Idle_vehicles amount = " + str(len(idle_vehicles)))
    # Update the location of vehicles with new assignments.
    for assi in assigned_tv:
        update_estimated_dropoff_time_of_requests_in_assignment(v=assi[1], path=assi[3], curr_time=curr_time, spc_dict=spc_dict)
        new_done_reqs = update_v_location(v=assi[1], path=assi[3], curr_time=curr_time, epoch_len=epoch_len, spc_dict=spc_dict, map_graph=map_graph)
        done_reqs.extend(new_done_reqs)
    # Writing down stats
    idle_rate = len(idle_vehicles) / len(v_list) * 100
    logging.info('idle vehicles : '+str(len(idle_vehicles))+'/'+str(len(v_list))+' = ' +str(idle_rate)+'%' )
    return idle_rate, done_reqs

    # def __init__(self, requests_list: Tuple[Request.Request, ...], vehicle_list: Tuple[Vehicle.Vehicle, ...], virtual_vehicle: Vehicle, map_graph: nx.Graph, current_time: datetime ,spc_dic


def update_estimated_dropoff_time_of_requests_in_assignment(v: Vehicle, path, curr_time: datetime.datetime, spc_dict):
    time_spent = datetime.timedelta(seconds=0)
    current_pos = copy.copy(v.curr_pos) #Don't want to change v's position in this function
    for next_stop_tuple in path:
        pickup = False
        if next_stop_tuple[1] == 'p':  # This is the pickup node
            next_stop_id = next_stop_tuple[0].origin
            pickup = True
        else:
            next_stop_id = next_stop_tuple[0].destination
            pickup = False

        time_to_next_stop = datetime.timedelta(seconds=spc_dict[current_pos][1][next_stop_id])
        time_spent += time_to_next_stop
        current_pos = next_stop_id

        if not pickup:
            next_stop_tuple[0].update_estimated_dropoff_time(curr_time + time_spent)

def update_v_location(v, path, curr_time, epoch_len, spc_dict, map_graph):
    # PATH IS (r_i,p/d)
    # Find location
    # time_spent is a time accumulator that we already spent traveling on the path.
    time_spent = datetime.timedelta(seconds=0)

    done_reqs = []
    # Iterating over each stop in the v path.
    # as long as we can reach the next stop within our time limit (epoch length) , we 'go' to the next stop , updating current position

    for count, next_stop_tuple in enumerate(path):
        next_stop_id = 0
        pickup = False
        # This if updates 'next_stop_id' , if its 'p' its the pickup node of request , else its the dropoff node of request.
        if next_stop_tuple[1] == 'p':  # This is the pickup node
            next_stop_id = next_stop_tuple[0].origin
            pickup = True
        else:
            next_stop_id = next_stop_tuple[0].destination
            pickup = False
        time_to_next_stop = datetime.timedelta(seconds=spc_dict[v.curr_pos][1][next_stop_id])
        if time_to_next_stop <= (epoch_len - time_spent):  # If we get to this stop within our epoch time limit.
            v.curr_pos = next_stop_id  # update v current position as the next stop.
            time_spent += time_to_next_stop  # accumulate the time spent going until here.
            if pickup:
                v.add_passenger(next_stop_tuple[0])
                next_stop_tuple[0].update_actual_pick_up_time(curr_time + time_spent)
            else:
                v.remove_passenger(next_stop_tuple[0])
                next_stop_tuple[0].update_actual_dropoff_time(curr_time + time_spent)
                done_reqs.append(next_stop_tuple[0])

        else:
            # "path_to_last_stop" is the path to the next stop on the path given to the function, and we can't reach that stop before the time limit (the next epoch ends)
            path_to_last_stop = copy.copy(spc_dict[v.curr_pos][0][next_stop_id])  # copy so we don't change spc_dict
            path_to_last_stop.pop(0)  # pop the first because that paths in spc_dict always start with the origin node

            # Instead of using spc_dict here, we can use the travel_time value that exists between each neighboring nodes.
            # That value already exists, as we always first run "add_edge_speeds()" and "add_edge_travel_times()" at the beginning of the simulation.
            # This way we save the time spc_dict_caregiver would spend calculating the paths and times from v.curr_pos to all of the graph.
            time_to_next_middle_stop = datetime.timedelta(seconds=map_graph[v.curr_pos][path_to_last_stop[0]][0]['travel_time'])

            while time_spent + time_to_next_middle_stop <= epoch_len:
                v.curr_pos = path_to_last_stop.pop(0)
                time_spent += time_to_next_middle_stop

                time_to_next_middle_stop = datetime.timedelta(seconds=map_graph[v.curr_pos][path_to_last_stop[0]][0]['travel_time'])

            # Now we add the remaining path to the vehicle's self.path.
            # We do that for the case in which a new trip was not assigned to the vehicle at the next epoch, and the vehicle should continue with the path he had.
            v.path = path[count:]  # TODO: make sure this works as planned

            break  # TODO: make sure this breaks the above for loop
    return done_reqs
"""
This function count the real ammount of requests created in this run
"""
def count_requests(epochs):
    result = 0
    for e in epochs:
        result += len(e)
    return result



def running_ny_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    curr_time = str_to_time(starting_time)
    # Virtual vehicle for algorithm purpose.
    virtual_v = Vehicle.Vehicle(0, time=curr_time)

    v_list = init_ny_vehicles(num_of_vehicles, current_time=curr_time)


    # Creating Shortest paths costs dictionary to hold those val's.
    # global spc_dict
    spc_dict = {}

    # Creating our map_graph.
    map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    # G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    map_graph = ox.add_edge_speeds(map_graph)
    map_graph = ox.add_edge_travel_times(map_graph)
    # Create logger.
    # logging.basicConfig(filename=str(datetime.datetime.now())+'.log',level=logging.INFO)
    logging.basicConfig(filename=str(datetime.datetime.now()).replace(':', '_')+'.log', level=logging.INFO) #Difference from above line makes it work on Windows - can't use ':' in filename in windows

    # Example :logging.info('This will get logged to a file')

    # Stats for log
    rate_of_epoch_sucsess = 0
    rate_of_run_sucsess = 0
    rate_of_idle_run = 0
    num_of_unserved_requests = 0
    sum_waiting_time = datetime.timedelta(seconds=0)
    sum_travel_delay = datetime.timedelta(seconds=0)
    num_of_served_reqs = 0
    logging.info('This run : ST= : '+ starting_time +', epoch_len = '+ str(epoch_len_sec) +' , num of epochs = '+ str(num_of_epochs) + ", num of vehicles = "+ str(num_of_vehicles) +'\n')
# def running_ny_sim(csv_path, num_of_vehicles, num_of_epochs, epoch_len_sec, starting_time=None):
    epochs = epoch_separator(requests_csv_path=csv_path, epoch_len_sec=epoch_len_sec, num_of_epochs=num_of_epochs, starting_time=starting_time,spc_dict=spc_dict, map_graph=map_graph )
    num_of_generated_requests = count_requests(epochs)
    added_time = datetime.timedelta(seconds=epoch_len_sec)
    # Working on each Epoch
    for count, epoch in enumerate(epochs):
        epoch_start_time = datetime.datetime.now()
        curr_time += added_time
        rv = RV_graph.RV_graph(requests_list=epoch, vehicle_list=v_list, virtual_vehicle=virtual_v, map_graph=map_graph, current_time=curr_time, spc_dict=spc_dict)
        rtv = RTV_graph.RTV_graph(rv_graph=rv, spc_dict=spc_dict, map_graph=map_graph, current_time=curr_time) # TODO Check if current time needed as well
        greedy = Greedy_assignment.Greedy_assingment(rtv)

        # TODO : here we need to assigning trips to vehicles
        epoch_set = set(epoch)
        r_nok = epoch_set - greedy.r_ok  # This is set difference , so only unserved requests are here.

        # Update log of this epoch
        logging.info(
            'E' + str(count) + ' : ' + str(curr_time - added_time) + ' to ' + str(curr_time) + '\n')
        # Update rate of sucsess
        rate_of_epoch_sucsess = len(greedy.r_ok) / len(epoch)  # The number of sent requests this epoch
        rate_of_run_sucsess += rate_of_epoch_sucsess
        logging.info('Epoch sucsess rate: ' + str(rate_of_epoch_sucsess*100)+'%')



        r_nok_ori_len = len(r_nok)
        r_nok_final_len = len(r_nok)

        if len(r_nok) != 0 and (len(epochs) - 1) != count :# If no r to append and this is not the last epoch.
            r_nok = filter_requests_time_to_pickup_over(r_nok, curr_time, added_time)
            r_nok_final_len = len(r_nok)
            epochs[count+1] = list(r_nok) + epochs[count+1] #TODO check validity

        num_of_unserved_requests += (r_nok_ori_len-r_nok_final_len)

        sizes_of_assigned_trips = [0 for _ in range(Vehicle.Vehicle.max_capacity)]
        for trip_tuple in greedy.assigned_tv:
            sizes_of_assigned_trips[len(trip_tuple[0].requests)-1] += 1
        print("Amounts of trips assigned, by sizes of trips = " + str(sizes_of_assigned_trips))



        # Update all vehicles with
        idle_rate, done_reqs = update_v_after_e(v_list, greedy.v_ok, greedy.assigned_tv, curr_time, added_time, spc_dict, map_graph)
        rate_of_idle_run+=idle_rate

        for r in done_reqs:
            sum_waiting_time += r.actual_pick_up_time - r.time_of_request
            sum_travel_delay += r.actual_dropoff_time - r.earliest_time_to_dest
        num_of_served_reqs += len(done_reqs)


        # update_penalties(r_nok) # TODO what to update?

        # Add requests from last epoch, that were assigned vehicles, but weren't picked-up yet
        if (len(epochs) - 1) != count: # First check we are not in the last epoch
            for r in greedy.r_ok:
                if r.actual_pick_up_time is None:
                    epochs[count + 1].insert(0, r)



        # logging.info()
        # What to do with all the data?

        # Last operation in each epoch.
        for v in v_list:
            v.clear_rv_after_epoch()

        epoch_end_time = datetime.datetime.now()
        logging.info("epoch number " + str(count) + " done. Time taken for this epoch = " + str(epoch_end_time-epoch_start_time) + ".\n")

    logging.info("STATS FOR THE WHOLE RUN"+'.\n')
    if num_of_epochs:
        logging.info("Mean rate of service : " + str(rate_of_run_sucsess / num_of_epochs) + "Total unserved : " + str(num_of_unserved_requests) + " out of " + str(num_of_generated_requests) + ".\n")
        logging.info("Mean idle vehicles for all epochs : "+ str(rate_of_idle_run/num_of_epochs)+".\n")
    logging.info("Total served : "+str(num_of_served_reqs)+" requests")
    if num_of_served_reqs>0:
        logging.info("Mean Travel Delay : "+str(sum_travel_delay/num_of_served_reqs))
    if num_of_served_reqs>0:
        logging.info("Mean Waiting time : "+str(sum_waiting_time/num_of_served_reqs))


    print('It is alive!')

"""
This are function for testing area
"""

def init_simple_vehicles(num_of_vehicles):
    # Open a log for the run.
    # logging.basicConfig(level=logging.INFO,filename='or_'+str(datetime.datetime.now()).replace(':', '_')+'.log')
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
            for i in range(5 * row, (5 * row) + 4):
                map_graph.add_edge(i, (i + 1), travel_times=1)

        for row in range(4):
            for i in range(5 * row, (5 * row) + 4):
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
    running_ny_sim('requests.csv', 50, 1000, 30, starting_time='2013-05-05 00:00:01')
    # print('====== is took : '+str(datetime.datetime.now() - start_time))






