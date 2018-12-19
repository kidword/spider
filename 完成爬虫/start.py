import os
import time



''' 启动一代一路机场数据和链家租房爬虫程序 '''
os.system(r'python D:\Users\dell\PycharmProjects\PY\完成爬虫\zufang.py')  # 链家租房数据爬取
time.sleep(30)
os.system(r'python D:\Users\dell\PycharmProjects\PY\完成爬虫\china.py')   # 一带一路国家机场数据
time.sleep(30)
os.system(r'python D:\Users\dell\PycharmProjects\PY\完成爬虫\flight.py')  # 世界机场数据

