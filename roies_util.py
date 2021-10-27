import datetime
from pandas import Timestamp
def str_to_time(s):
    t = Timestamp(s)
    return t.to_pydatetime()