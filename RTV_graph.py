import  RV_graph


def two_trips_to_unique_tuple(trip1, trip2):
    return tuple(set(trip1 + trip2))


class RTV_graph :

    def __init__(self,rv_graph):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(rv_graph.nodes()) # We need all nodes from rv_graph
        # We tested to make sure, and copying nodes from another graph, like above, doesn't copy the edges between them as well

        vehicle_nodes = rv_graph.nodes(type="v")

        for v in vehicle_nodes:
            # algo1()

            # Lets start with trip of size one (kind of like pesudo code or concept code)
            requests_connected_to_v = rv_graph.edges(v)
            v_taos = []
                # All the taos, the groups of trips the current vehicle can make. The groups in it are groups of trips of the same size.
                # Will be later added, or merged, to the tao of the whole RTV_graph
            taoK = [] #current_tao. from tao_1 to tao_i, where i is the max amount of people the vehicle can have on board
            found_trip_for_last_taoK = False

            # In the case of tao_1, all edges connected to v, create a trip
            for r in requests_connected_to_v:
                taoK.append((r))
                found_trip_for_last_taoK = True

            # After we are finished adding all the trips to taoK, we append them to v_taos
            v_taos.append(taoK)
            taoK = []

            # In the case of tao_2, we go over every pair of trips of tao_1, trips of size 1 having 1 request in them, and check if -
            #   A. The 2 requests have an edge between them in the RV_graph
            #   B. The travel() function returns "true" (i.e. a route exists for both of the requests + the vehicle)
            # If so, we add this trip (of size 2) to taoK, to be added later to v_taos
            if found_trip_for_last_taoK:
                found_trip_for_last_taoK = False
                for r1 in range(len(requests_connected_to_v)-1): #for each trip in the previous taoK
                    for r2 in range(r1+1, len(requests_connected_to_v)):
                        if(rv_graph.has_edge(requests_connected_to_v[r1], requests_connected_to_v[r2])):
                            requests = (copy.copy(requests_connected_to_v[r1]), copy.copy(requests_connected_to_v[r2]))
                            returned_value = TripAlgo.travel(v, requests)
                            if returned_value[0] == True:
                                taoK.append((r1, r2))
                                found_trip_for_last_taoK = True
                v_taos.append(taoK)
                taoK = []

                # Now, the general case, trips of size K.
                # We take each pair of Trips of the previous size, k-1, and check if the size of the union of their trips equals k.
                # If so, we check the following -
                #   We make a union of the requests of the 2 trips.
                #   We check that for every request we remove from that union, there exists a trip with that set of requests, in the previous taoK
                #   (that will be in v_taos[-1])
                # Then, if that condition is true, check that this vehicle and the requests of the original union (that of the 2 trips), returns a valid answer form the function travel()
                # If so, add the the trip (made by the mentioned union) to taoK.

                for k in range(3, Vehicle.max_capacity - len(v.passengers) + 1):
                    if found_trip_for_last_taoK:
                        found_trip_for_last_taoK = False
                        for t1 in range(len(v_taos[-1])-1):
                            trip1 = v_taos[-1][t1]
                            for t2 in range(t1+1, len(v_taos[-1])):
                                trip2 = v_taos[-1][t2]
                                # We have the 2 trips we want to check, now we check the 1st condition - size of their union is k
                                new_trip = two_trips_to_unique_tuple(trip1 + trip2)
                                if len(new_trip) == k:







    def algo1(self,vehicleList):
        tao = [] # Tao is epmty list
        taoK = [] #Tao trips of size k
        for  v in vehicleList :
            taoK.clear()
            for rve in self.graph.rvEdges :
                # trip =


