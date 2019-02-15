import os

os.system(r'python D:\Users\dell\PycharmProjects\PY\lj_data\esf.py')
os.system(r'python D:\Users\dell\PycharmProjects\PY\lj_data\thread_lat.py')
os.system(r'python D:\Users\dell\PycharmProjects\PY\lj_data\lj_update.py')


'''
esf.py:爬取链家数据后保存到数据库中，删除重复的数据
thread_lat：将数据库中数据再次进行经纬度爬取
lj_update：将单价不同的数据保存起来
'''