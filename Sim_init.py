
# This class hold Several parameters to init a simulation
import datetime

class Sim_init:
    #Vehicle stats
    fleet_size : int # Fixed fleet size for simulation.
    v_cap : int # Vehicle capacity , maximun num of passengers.
    #Times
    #datetime.timedelta documentation :A duration expressing the difference between two date, time, or datetime instances to microsecond resolution.
    max_delay : datetime.timedelta # The difference between the drop off time and minimal time to reach destination.==: delta = Request.toed - Requst.toe

