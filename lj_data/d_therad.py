from urllib import parse
import requests
import json
import pymysql as py
from fake_useragent import UserAgent
import datetime

ua = UserAgent()
now_time = datetime.datetime.now().strftime('%Y-%m-%d')


# 读取数据库数据
def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')


conn = getmysql()
cur = conn.cursor()
cn = cur.execute('select * from lj_spider where dtime="{}"'.format(now_time))
rows = cur.fetchall()
rows = list(rows)


def getname():
    name_lis = []
    for lis in rows:
        name_lis.append(list(lis))
    return name_lis


l = getname()
error = []


def getarea():
    for name in l:
        names = name[1] + name[2]
        query = {
            'key': 'f247cdb592eb43ebac6ccd27f796e2d2',
            'address': names,
            'output': 'json',
        }
        base = 'http://api.map.baidu.com/geocoder?'
        url = base + parse.urlencode(query)
        headers = {"User-Agent": ua.random}
        doc = requests.get(url, headers=headers)
        s = doc.content.decode('utf-8')  # 一定要解码！！！！
        try:
            jsonData = json.loads(s)
            lat = jsonData['result']['location']['lat']
            lng = jsonData['result']['location']['lng']
            print(name[1], name[2], name[3], name[4], name[5], name[6], lng, lat)
            cur = conn.cursor()
            sql = "insert into lj_test(qu,address,apartment,area,d_price,z_price,lat,lon,dtime) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (name[1], name[2], name[3], name[4], name[5], name[6], lat, lng, now_time)
            cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            error.append(names)
            print(e)


getarea()

print(error)
conn.close()
