import datetime
import unittest
import Runnin_Sim
from roies_util import str_to_time
import osmnx as ox


class Test_Running_sim(unittest.TestCase):
    def test_init_num_of_v(self):
        v1 = Runnin_Sim.init_ny_vehicles(5 ,datetime.datetime.now())
        v2 = Runnin_Sim.init_ny_vehicles(0,datetime.datetime.now())
        v3 = Runnin_Sim.init_ny_vehicles(6,datetime.datetime.now())
        self.assertEqual(len(v1), 5)  # add assertion here
        self.assertEqual(len(v2), 0)
        self.assertEqual(v1[0].id,0)
        self.assertEqual(v3[0].id,5)

    def test_epoch_seperator_from_start(self):
        spc_dict = {}
        # Creating our map_graph.
        map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        # G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        map_graph = ox.add_edge_speeds(map_graph)
        map_graph = ox.add_edge_travel_times(map_graph)
        epochs=Runnin_Sim.epoch_separator(requests_csv_path='requests.csv',epoch_len_sec=5,num_of_epochs=2,map_graph=map_graph,spc_dict=spc_dict)
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-05 00:00:01'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request,str_to_time('2013-05-05 00:00:06'))
            self.assertGreaterEqual(r.time_of_request, str_to_time('2013-05-05 00:00:01'))

        for r in epochs[1]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-05 00:00:11'))
            self.assertGreaterEqual(r.time_of_request, str_to_time('2013-05-05 00:00:06'))
    def test_epoch_seperator_from_mid(self):
        spc_dict = {}
        # Creating our map_graph.
        map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        # G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        map_graph = ox.add_edge_speeds(map_graph)
        map_graph = ox.add_edge_travel_times(map_graph)
        epochs=Runnin_Sim.epoch_separator(requests_csv_path='requests.csv',epoch_len_sec=5,num_of_epochs=2,map_graph=map_graph,spc_dict=spc_dict,starting_time='2013-05-06 00:00:00')
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-06 00:00:00'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-06 00:00:05'))
            self.assertGreaterEqual(r.time_of_request, str_to_time('2013-05-06 00:00:00'))

        for r in epochs[1]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-06 00:00:11'))
            self.assertGreaterEqual(r.time_of_request, str_to_time('2013-05-06 00:00:06'))
    def test_epoch_seperator_until_end(self):
        spc_dict = {}
        # Creating our map_graph.
        map_graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        # G = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
        map_graph = ox.add_edge_speeds(map_graph)
        map_graph = ox.add_edge_travel_times(map_graph)
        epochs=Runnin_Sim.epoch_separator(requests_csv_path='requests.csv',epoch_len_sec=30,num_of_epochs=2,map_graph=map_graph,spc_dict=spc_dict,starting_time='2013-05-11 23:56:59')
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-11 23:57:00'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-11 23:57:29'))
            self.assertGreaterEqual(r.time_of_request, str_to_time('2013-05-11 23:57:00'))


    """
    This section tests simple graph
    """
    """
    def test_simple_graph_construction(self):
        v1=Runnin_Sim.init_simple_vehicles(1)
        map_graph = Runnin_Sim.create_simple_graph(1)
        print('done')
        self.assertEqual(len(map_graph.nodes()),25) 
        """







if __name__ == '__main__':
    unittest.main()
