import networkx as nx
import copy


def spc_dict_caregiver(spc_dict, map_graph, source_node):
    if source_node in spc_dict:
        return
    # else
    paths = nx.single_source_dijkstra_path(map_graph, source_node, weight='travel_times')
    costs = nx.single_source_dijkstra_path_length(map_graph, source_node, weight='travel_times')
    spc_dict[source_node] = [copy.copy(paths), copy.copy(costs)]
    # print('spc_dict fuckgiver :'+str(source_node))
