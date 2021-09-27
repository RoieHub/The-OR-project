import  RV_graph
import Trip
import TripAlgo

def two_trips_to_unique_tuple(trip1, trip2):
    return tuple(set(trip1 + trip2))


class RTV_graph :

    def __init__(self,rv_graph):
        self.graph = nx.Graph()
        self.rv_graph = rv_graph


        # We need all nodes from rv_graph.
        # data=True means that we will get a tuple for each node in the rv_graph.nodes.
        # Using the add_nodes_from on that will also copy the attributes of the nodes, such as type=v\r, which we need.
        # We also tested to make sure, and copying nodes from another graph, like below, doesn't copy the edges between them as well
        self.graph.add_nodes_from(rv_graph.nodes(data=True))

        # vehicle_nodes = rv_graph.nodes(type="v")
        vehicle_nodes = [x for x,y in rv_graph.nodes(data=True) if y['type'] == 'v']

        tao = [[] for _ in range(Vehicle.max_capacity)]


        # Now for each vehicle
        for v in vehicle_nodes:
            v_taos = algo1(v)
            # Now merge all of v_taos entries to main tao.
            # In the returned v_taos, we iterate over every taoK (group of trips of size k), and check if this trip already exists in the graph.
            # If it exists - that means that trip already exists. Just add the relevant edges to it.
            # If it doesn't - add a trip node to the graph and add the relevant edges to it.
            for k in range(len(v_taos)):
                for t in range(len(v_taos[k])):
                    trip = None
                    try: #if the graph already has that trip this part of the code will run - only add relevant edges to the graph, not the trip node itself
                        trip = self.graph.nodes[v_taos[k][t][0]]
                    except:
                        pass

                    if trip is not None:
                        self.graph.add_edge(trip, v)
                    else:# In case the trip isn't in the graph yet, we need to add it and edges from it's rides to it and from it to the current vehicle, as it can do this trip

                        tao[k].append(v_taos[k][t][0])

                        # Add the trip node to the graph.
                        trip_node = Trip.Trip(v_taos[k][t][0])
                        self.graph.add_node(trip_node, data=trip_node, type='t')

                        # Add edges between the trip and the requests
                        for r in trip_node.requests:
                            self.graph.add_edge(r, trip_node)

                        # Add the edge between the trip and the vehicle, with the weight of the trip for this vehicle (i.e. the accumulated delay caused to the passengers in it)
                        self.graph.add_edge(trip_node, v, weight=v_taos[k][t][1])







    def algo1(self,v):
        # algo1()


        requests_connected_to_v = [x[1] for x in self.rv_graph.edges() if x[0] == v]
        v_taos = []
        # All the taos, the groups of trips the current vehicle can make. The groups in it are groups of trips of the same size.
        # Will be later added, or merged, to the tao of the whole RTV_graph
        taoK = []  # current_tao. from tao_1 to tao_i, where i is the max amount of people the vehicle can have on board

        # In the case of tao_1, all edges connected to v, create a trip
        for r in requests_connected_to_v:
            taoK.append(Trip.Trip(requests=(r)))

        # After we are finished adding all the trips to taoK, we append them to v_taos
        v_taos.append(taoK)
        taoK = []

        # In the case of tao_2, we go over every pair of trips of tao_1, trips of size 1 having 1 request in them, and check if -
        #   A. The 2 requests have an edge between them in the RV_graph
        #   B. The travel() function returns "true" (i.e. a route exists for both of the requests + the vehicle)
        # If so, we add this trip (of size 2) to taoK, to be added later to v_taos

        for r1 in range(len(requests_connected_to_v) - 1):  # for each trip in the previous taoK
            for r2 in range(r1 + 1, len(requests_connected_to_v)):
                if (self.rv_graph.has_edge(requests_connected_to_v[r1], requests_connected_to_v[r2])):
                    requests = (copy.copy(requests_connected_to_v[r1]), copy.copy(requests_connected_to_v[r2]))
                    returned_value = TripAlgo.travel(v, requests, sp_dict)
                    if returned_value[0] == True:
                        taoK.append(((r1, r2), returned_value[1]))
        v_taos.append(taoK)
        taoK = []

        # Now, the general case, trips of size K.
        # We take each pair of Trips of the previous size, k-1, and check (CHECK 1) if the size of the union of their trips equals k.
        # If so, we check the following -
        #   We make a union of the requests of the 2 trips.
        #   We check (CHECK 2) that for every request we remove from that union, there exists a trip with that set of requests, in the previous taoK
        #   (that will be in v_taos[-1])
        # Then, if that condition is true, check (CHECK 3) that this vehicle and the requests of the original union (that of the 2 trips), returns a valid answer form the function travel()
        # If so, add the the trip (made by the mentioned union) to taoK.

        for k in range(3, Vehicle.max_capacity - len(v.passengers) + 1):
            for t1 in range(len(v_taos[-1]) - 1):
                trip1 = v_taos[-1][t1]
                for t2 in range(t1 + 1, len(v_taos[-1])):
                    trip2 = v_taos[-1][t2]
                    # We have the 2 trips we want to check, now we check CHECK 1
                    new_trip = two_trips_to_unique_tuple(trip1, trip2)
                    if len(new_trip) == k:
                        new_trip.sort() #We sort the trip, to make sure that later, when checking if a sub_trip exists within taok-1 (v_taos[-1]), we will not miss because of ordering
                        # CHECK 2
                        condition = True
                        # The above boolean variable is used to check if the condition CHECK 2 is true or not. It will change to false in case it doens't, and we break out of the for loop to not waste time.
                        for r in new_trip:
                            sub_trip = copy.copy(new_trip)
                            sub_trip.remove(r)
                            if sub_trip not in v_taos[-1]:
                                condition = False
                                break
                        if condition:
                            # CHECK 3
                            returned_value = TripAlgo.travel(v, new_trip, sp_dict)
                            if returned_value[0] == True:
                                taoK.append((new_trip, returned_value[1]))
            v_taos.append(taoK)
            taoK = []
        return v_taos

