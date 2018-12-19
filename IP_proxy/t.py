import random
st = "07:30:00"
et = "09:30:33"


def time2seconds(t):
    h,m,s = t.strip().split(":")
    print(h,m,s)
    return int(h) * 3600 + int(m) * 60 + int(s)


def seconds2time(sec):
    m,s = divmod(sec,60)
    h,m = divmod(m,60)
    return "%02d:%02d:%02d" % (h,m,s)

sts = time2seconds(st) #sts==27000
ets = time2seconds(et) #ets==34233

rt = random.sample(range(sts,ets),10)
#rt == [28931, 29977, 33207, 33082, 31174, 30200, 27458, 27434, 33367, 30450]

rt.sort() #对时间从小到大排序


for r in rt:
    print(seconds2time(r))