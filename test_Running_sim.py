import unittest
import Runnin_Sim
from roies_util import str_to_time


class Test_Running_sim(unittest.TestCase):
    def test_init_num_of_v(self):
        v1 = Runnin_Sim.init_ny_vihecles(5)
        v2 = Runnin_Sim.init_ny_vihecles(0)
        v3 = Runnin_Sim.init_ny_vihecles(6)
        self.assertEqual(len(v1), 5)  # add assertion here
        self.assertEqual(len(v2), 0)
        self.assertEqual(v1[0].id,0)
        self.assertEqual(v3[0].id,5)

    def test_epoch_seperator_from_start(self):
        epochs=Runnin_Sim.epoch_separator('clean_2013.csv',5,2)
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-01 00:00:01'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request,str_to_time('2013-05-01 00:00:06'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-01 00:00:11'))

    def test_epoch_seperator_from_mid(self):
        epochs=Runnin_Sim.epoch_separator('clean_2013.csv',5,2,str_to_time('2013-05-05 00:00:06'))
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-05 00:00:06'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request,str_to_time('2013-05-05 00:00:11'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-05 00:00:16'))
    def test_epoch_seperator_until_end(self):
        epochs=Runnin_Sim.epoch_separator('clean_2013.csv',5,2,str_to_time('2013-05-11 23:58:00'))
        self.assertEqual(epochs[0][0].time_of_request, str_to_time('2013-05-11 23:58:00'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request,str_to_time('2013-05-11 23:59:00'))
        for r in epochs[0]:
            self.assertLessEqual(r.time_of_request, str_to_time('2013-05-11 23:59:00'))






if __name__ == '__main__':
    unittest.main()
