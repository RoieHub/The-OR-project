import copy

import networkx as nx
import RV_graph
import Trip
import TripAlgo
import Vehicle


def two_trips_to_unique_set(trip1, trip2):
    return set(trip1.requests + trip2.requests)


class RTV_graph:

    def __init__(self, rv_graph, spc_dict):
        self.map_graph = rv_graph.map_graph
        self.graph = nx.Graph()
        self.rv_graph = rv_graph
        self.spc_dict = spc_dict

        # We need all nodes from rv_graph.
        # data=True means that we will get a tuple for each node in the rv_graph.nodes.
        # Using the add_nodes_from on that will also copy the attributes of the nodes, such as type=v\r, which we need.
        # We also tested to make sure, and copying nodes from another graph, like below, doesn't copy the edges between them as well
        self.graph.add_nodes_from(rv_graph.nodes(data=True))

        # vehicle_nodes = rv_graph.nodes(type="v")
        vehicle_nodes = [x for x, y in rv_graph.nodes(data=True) if y['type'] == 'v']

        self.tao = [[] for _ in range(Vehicle.max_capacity)]

        # Now for each vehicle
        for v in vehicle_nodes:
            v_taos = self.algo1(v)
            # Now merge all of v_taos entries to main tao.

            # There is a problem.
            # The "algo1" uses TripAlgo, and TripAlgo computes the delay for all the requests in the trip AND THE DELAY FOR THE PASSANGERS ALREADY ON THE CAR.
            # The weights on the edges of type TV in the RTV graph should be only the delay caused to the requests in the trip, without the delay to the passengers already in the car.
            # So the next bit of code computes the delay of the passengers on the vehicle, so we can reduce that later from the delay reported by algo1, for each trip.
            # We note that the path that algo1 gave for a trip might change the order in which the passengers already on the vehicle get dropedoff.
            # Some of the requests in trip might be picked-up before they get droppedoff, and they might even just change the order between them.
            # Having said that, that doesn't matter for the purpose of this part of the code - reducing the delay of the passengers already on board the vehicle.
            # That is because the passengers already on board have a value in their "estimated_dropoff_time", and we calculate delay for them based on that.
            # Because we must give them service that will get them to their destination before their "estimated_dropoff_time", even if the path will change from the path that set the "estimated_dropoff_time",
            # the new path will be at least as good as the previous for them (safe to assume not better, as if a better path existed, it would have been choosen first)
            # Meaning that the delay for the passengers of the vehicle will be the same in the new path as it was in the old one.

            # So, we set the variable "delay_of_passengers_of_v" to 0
            # and for each passenger on the vehicle, we calc his expected delay (it is estimated_dropoff_time - earliest_time_to_dest ===> the time added to him because he used our services, instead of driving a private car)
            # There shouldn't be any passengers with None as their estimated_dropoff_time, but checking to make sure, as if it is none, it could damage our calculation.
            delay_of_passengers_of_v = 0
            for p in v.passengers:
                if p.estimated_dropoff_time is not None:
                    delay_of_passengers_of_v += p.estimated_dropoff_time - p.earliest_time_to_dest

            # Now back to merging all of v_taos entries to main tao.
            # In the returned v_taos, we iterate over every taoK (group of trips of size k), and check if this trip already exists in the graph.
            # If it exists - that means that trip already exists. Just add the relevant edges to it.
            # If it doesn't - add a trip node to the graph and add the relevant edges to it.
            for k in range(len(v_taos)):
                for t in range(len(v_taos[k])):
                    trip = None
                    try:  # if the graph already has that trip this part of the code will run - only add relevant edges to the graph, not the trip node itself
                        trip = self.graph.nodes[v_taos[k][t][0]]['data']
                    except:
                        pass

                    if trip is not None:
                        self.graph.add_edge(trip, v, weight=(v_taos[k][t][1] - delay_of_passengers_of_v), type="tv")
                        trip.add_vehicle_candidate((v, (v_taos[k][t][1] - delay_of_passengers_of_v)))
                    else:  # In case the trip isn't in the graph yet, we need to add it and edges from it's rides to it and from it to the current vehicle, as it can do this trip
                        # Get the new trip object
                        new_trip = v_taos[k][t][0]

                        # Add to the new trip the vehicle as a candidate, along with the cost associated with it.
                        # Then add the trip to the variable tao.
                        new_trip.add_vehicle_candidate((v, (v_taos[k][t][1] - delay_of_passengers_of_v)))
                        self.tao[k].append(new_trip)

                        # Add the new trip to the graph, as a node of the graph.

                        self.graph.add_node(new_trip, data=new_trip, type='t')

                        # Add edges between the trip and the requests
                        for r in new_trip.requests:
                            self.graph.add_edge(r, new_trip, type='rt')

                        # Add the edge between the trip and the vehicle, with the weight of the trip for this vehicle (i.e. the accumulated delay caused to the passengers in it)
                        self.graph.add_edge(new_trip, v, weight=(v_taos[k][t][1] - delay_of_passengers_of_v), type="tv")

    def algo1(self, v):
        # algo1()

        requests_connected_to_v = [x[1] for x in self.rv_graph.edges() if x[0] == v]
        v_taos = []
        # All the taos, the groups of trips the current vehicle can make. The groups in it are groups of trips of the same size.
        # Will be later added, or merged, to the tao of the whole RTV_graph
        taoK = []  # current_tao. from tao_1 to tao_i, where i is the max amount of people the vehicle can have on board

        # In the case of tao_1, all edges connected to v, create a trip
        for r in requests_connected_to_v:
            # No need to calc the delay by using TripAlgo, as that was already calculated for each requests_connected_to_v.
            # The fact that the request is connected to v, means that tripAlgo checked it, and returned true, meaning v can take the request.
            # Also, the delay will be on the edge connecting the request and the vehicle in the RV_graph.

            # The following line gets the weight of the edge from the graph - from all the edges, take the one between v and r, take the weight in it.
            # This will have to be put in to a list, so we take the first and only value in there, the weight we wanted.
            weight = [z['weight'] for x, y, z in self.rv_graph.edges(data=True) if (x == v) & (y == r)][0]
            taoK.append((Trip.Trip(requests=(r)), weight))

        # After we are finished adding all the trips to taoK, we append them to v_taos
        v_taos.append(copy.copy(taoK))
        taoK = []

        # In the case of tao_2, we go over every pair of trips of tao_1, trips of size 1 having 1 request in them, and check if -
        #   A. The 2 requests have an edge between them in the RV_graph
        #   B. The travel() function returns "true" (i.e. a route exists for both of the requests + the vehicle)
        # If so, we add this trip (of size 2) to taoK, to be added later to v_taos

        for r1 in range(len(requests_connected_to_v) - 1):  # for each trip in the previous taoK
            for r2 in range(r1 + 1, len(requests_connected_to_v)):
                if self.rv_graph.has_edge(requests_connected_to_v[r1], requests_connected_to_v[r2]):
                    requests = (requests_connected_to_v[r1], requests_connected_to_v[r2])
                    returned_value = TripAlgo.travel(v, requests, self.map_graph, self.spc_dict)
                    if returned_value[0] == True:
                        taoK.append((Trip.Trip(r1, r2), returned_value[1]))
        v_taos.append(copy.copy(taoK))
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
                trip1 = v_taos[-1][t1][0]
                for t2 in range(t1 + 1, len(v_taos[-1])):
                    trip2 = v_taos[-1][t2][0]
                    # We have the 2 trips we want to check, now we check CHECK 1
                    new_trip_requests = two_trips_to_unique_set(trip1, trip2)
                    if len(new_trip_requests) == k:
                        new_trip_requests.sort()  # We sort the trip, to make sure that later, when checking if a sub_trip exists within taok-1 (v_taos[-1]), we will not miss because of ordering
                        new_trip_requests = tuple(new_trip_requests)  # make it to a tuple so make sure it isn't changed
                        # CHECK 2
                        condition = True
                        # The above boolean variable is used to check if the condition CHECK 2 is true or not. It will change to false in case it doens't, and we break out of the for loop to not waste time.
                        for r in new_trip_requests:
                            sub_trip_requests = list(
                                copy.copy(new_trip_requests))  # should be a list so we can remove the relevant request r
                            sub_trip_requests.remove(r)
                            if Trip.Trip(sub_trip_requests) not in (x[0] for x in v_taos[-1]):
                                condition = False
                                break
                        if condition:
                            # CHECK 3
                            returned_value = TripAlgo.travel(v, new_trip_requests, self.map_graph, self.spc_dict)
                            if returned_value[0] == True:
                                taoK.append((Trip.Trip(new_trip_requests), returned_value[1]))
            v_taos.append(copy.copy(taoK))
            taoK = []
        return v_taos
