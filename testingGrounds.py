import copy
import datetime

import Request
import RTV_graph
import RV_graph
import Trip
import TripAlgo
import Vehicle
import osmnx as ox
import networkx as nx
import time

# import pickle
import _pickle as pickle
from multiprocessing import Process, Manager

'''
unpickeling in a different process, takes way less memory and works in a few seconds - 
https://stackoverflow.com/questions/35360715/after-unpickling-system-use-a-lot-of-ram

if you get error - runtime error, something about not main process - 
https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing

error iteritems() doesn't exists, use items() instead - 
https://stackoverflow.com/questions/10458437/what-is-the-difference-between-dict-items-and-dict-iteritems-in-python2


'''


def load_pickle(filename, data):
    with open(filename, 'rb') as file:
        data_pkl = pickle.load(file)
    for key, val in data_pkl.items():
        data[key] = val


if __name__ == '__main__':




    # # G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
    # # G = ox.add_edge_speeds(G)
    # # G = ox.add_edge_travel_times(G)
    # #
    # # start = time.time()
    # # path = dict(nx.all_pairs_bellman_ford_path(G), weight='travel_times')
    # # end = time.time()
    # # print (end-start)
    #
    # manager = Manager()
    # data_dict = manager.dict()
    # p = Process(target=load_pickle, args=("all_paths_nyc_part0.pickle", data_dict))
    # start = time.time()
    # p.start()
    # p.join()
    # end = time.time()
    # print(end - start)
    #
    # # print(len(data_dict))
    # p = Process(target=load_pickle, args=("all_paths_nyc_part1.pickle", data_dict))
    # start = time.time()
    # p.start()
    # p.join()
    # end = time.time()
    # print(end - start)
    #
    # p = Process(target=load_pickle, args=("all_paths_nyc_part2.pickle", data_dict))
    # start = time.time()
    # p.start()
    # p.join()
    # end = time.time()
    # print(end - start)
    # # print(len(data_dict))

    # print("hello world")
    G = nx.Graph()
    r1 = Request.Request(0, 1, datetime.datetime.now())
    r2 = Request.Request(1, 2, datetime.datetime.now())
    t1 = Trip.Trip((r1, r2))
    G.add_node(t1, data=t1)
    a = 0
    # for n in G.nodes:
    #     a=n
    #     print(type(n))
    # if a==t1:
    #     print("equals")
    # else:
    #     print("not equal")
    trip_from_the_graph_probably_empty = None
    try:
        trip_from_the_graph_probably_empty = G.nodes[Trip.Trip(r1)]
    except:
        pass

    trip_from_the_graph = G.nodes[Trip.Trip((r1, r2))]['data']
    trip_from_the_graph_2 = G.nodes[Trip.Trip((r1, r2))]
    trip_from_the_graph_2_data = trip_from_the_graph_2['data']
    # trip_from_the_graph.requests = (r1) #this line was to check if we get a refrence or copy when getting node back from the graph. Changing what we get back. Changed the original trip. So indeed a refrence.


    G.add_edge(trip_from_the_graph, r1, weight = 42)
    weight = [z['weight'] for x, y, z in G.edges(data=True) if ((x==trip_from_the_graph) & (y==r1))][0]
    for x,y,z in G.edges(data=True):
        print(z['weight'])

    for edge in G.edges(data=True):
        print(edge)



    if trip_from_the_graph == t1:
        print("equals")
    else:
        print("not equal")

    # print("len(trip_from_the_graph) = " + str(len(trip_from_the_graph)))
    # for t in trip_from_the_graph:
    #     print("type(t) = " + str(type(t)))
    print("type(trip_from_the_graph) = " + str(type(trip_from_the_graph)))

    # v1 = Vehicle.Vehicle(5)
    # G.add_node(r1)
    # G.add_node(r2)
    #
    # G.add_node(v1)
    #
    # G.add_edge(r1, r2)
    # # my_nodes = G.nodes()
    # for n in G.nodes():
    #     print(n)
    # for e in G.edges():
    #     print(e[0].origin)
