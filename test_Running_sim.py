import unittest
import Runnin_Sim


class Test_Running_sim(unittest.TestCase):
    def test_init_num_of_v(self):
        v1 = Runnin_Sim.init_ny_vihecles(5)
        v2 = Runnin_Sim.init_ny_vihecles(0)
        self.assertEqual(len(v1), 5)  # add assertion here
        self.assertEqual(len(v1), 0)



if __name__ == '__main__':
    unittest.main()
