import time
import random

sj = random.choice(range(10,20))
start = 1509465600 + 21600
end_time = 1509465600 + (22 * 3600)

def settime(st,ed,sj):
    rt = random.sample(range(st,ed),sj)
    return sorted(rt)
print((settime(start,end_time,sj)))

timeArr=settime(start,end_time,sj)

for i in range(0, len(timeArr)):

    pass
# jg = random.choice(range(100, 1000))
# oneday = 60*60*24  # 一天时间戳
# end_time = start+oneday
#
# timearray = time.localtime(end_time)
# dtime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
# print(dtime)
#
# now = int(time.time())
# print((now-start)/(60*60*24))
# jg_day = (now-start)/(60*60*24)
# for i in range(int(jg_day)):
#     start += oneday
#     for k in range(10):
#         pass