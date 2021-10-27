import datetime

# Old ver , with pandas middleman middleman
def str_to_time(s):
    t = datetime.strptime(s, '%y-%m-%d %H:%M:%S')
    return t



'''def str_to_time(s):
    t = Timestamp(s)
    return t.to_pydatetime()'''
