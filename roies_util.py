from datetime import datetime
from pandas import Timestamp

# Old ver , with pandas middleman middleman
'''def str_to_time(s):
    ns = s.replace("-",'/')
    t = datetime.strptime(ns,'%Y/%m/%d %H:%M:%S')
    return t'''

#2013-05-05 00:00:01
#2013-05-11 23:52:58

def str_to_time(s):
    t = Timestamp(s)
    return t.to_pydatetime()
