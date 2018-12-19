'''
获取222个国家机场数据，起飞机场国家名称、起飞机场名称、起飞机场代码、起飞机场经度、起飞机场纬度
降落机场国家名称、降落机场名称、降落机场代码、降落机场经度、降落机场纬度 存mysql 数据库中
'''
import numpy as np
import pymysql as py
import requests
import json
import re
import time
import pandas as pd
import random
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   # 2018-07-26 14:55:07
# getConnection函数：连接数据库
def getConnection():
    return py.connect(host='localhost', user='root', password='hh226752',db = 'flightradar24', charset = 'utf8' )

# 加载数据库中数据
conn = getConnection()
cur = conn.cursor()
cn = cur.execute('select Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon from test')

rows = cur.fetchall()
rows = list(rows)
#print(rows)

url = 'https://www.flightradar24.com/data/airports/{}/routes'
Airports_code1 = []
for i in rows:
    Airports_code1.append(list(i))
#print(Airports_code1)
Airports_code2 = []  #得到所有的机场代码连接url
None_info_Airport = [] # 没有航班信息的机场代码
xin_info_airport = []
for i in Airports_code1:
    try:
        urls = url.format(i[2])
        headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                   "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                   "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                   "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                   ]

        response = requests.get(url=url, headers={'User-Agent': random.choice(headers)}, verify=False)
        html = response.text
        L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
        ss = re.findall('{.*?}', L)
        for j in ss:
            l = json.loads(j)
            flg_code = l['iata'] # 机场代码
            flg_name = l['name'] # 机场名称
            flg_city = l['city'] # 机场所在城市
            flg_country = l['country'] # 机场所在国家
            flg_lat = l['lat'] # 机场的经度
            flg_lon = l['lon'] # 机场的纬度
            sql_insert = "insert into flight_xin_copy(Take_off_airport_country,Take_off_airport_name,Take_off_airport_code,Take_off_airport_alt,Take_off_airport_lon,Landing_airport_country,Landing_airport_name,Landing_airport_code,Landing_airport_city,Landing_lat,Landing_lon) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #param = (i[0],i[1],i[2],i[3],i[4],flg_country,flg_name,flg_code,flg_city,flg_lat,flg_lon)
            #param = [i[0],i[1],i[2],i[3],i[4],flg_country,flg_name,flg_code,flg_city,flg_lat,flg_lon]
            #xin_info_airport.append(param)
            #cur.execute(sql_insert,param)
            conn.commit()
            print(i[0],i[1],i[2],i[3],i[4],flg_country,flg_name,flg_code,flg_city,flg_lat,flg_lon)

    except AttributeError:
        l = [i[0],i[1],i[2],i[3],i[4]]
        None_info_Airport.append(l)
        print('没有航线信息的机场：',i[2])

# 写入csv文件中
# name = ['起飞机场国家','起飞机场名称','起飞机场代码','起飞机场经度','起飞机场纬度']
# test = pd.DataFrame(columns=name, data=None_info_Airport)
# test.to_csv(r'D:\机场新数据信息列表.csv')


# name = ['起飞机场国家','起飞机场名称','起飞机场代码','起飞机场经度','起飞机场纬度']
# test = pd.DataFrame(columns=name, data=None_info_Airport)
# test.to_csv(r'D:\NO机场信息列表.csv')
# 将 [[str1],[str2],[str3]]———> 装换成[str1,str2,str3]
conn.commit()
conn.close()

# 判断最新的 i[2], flg_code 是否同时存在一个列表中，存在就不添加，不存在就添加新数据


