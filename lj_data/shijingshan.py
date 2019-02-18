from urllib import parse
import requests
import json
import pymysql as py
from fake_useragent import UserAgent
import datetime
import time
from retrying import retry
ua = UserAgent()
now_time = datetime.datetime.now().strftime('%Y-%m-%d')


# 读取数据库数据
def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')


conn = getmysql()
cur = conn.cursor()
# cn = cur.execute('select * from lj_spider where dtime="{}"'.format(now_time))
cn = cur.execute('select * from lj_spider where qu="石景山区" and dtime="{}"'.format(now_time))
rows = cur.fetchall()
rows = list(rows)


def getname():
    name_lis = []
    for lis in rows:
        name_lis.append(list(lis))
    return name_lis
l = getname()
error = []


@retry(stop_max_attempt_number=5)
def run():
    n = 1
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
            sql = "insert into lj_xb(qu,address,apartment,area,d_price,z_price,lat,lon,dtime) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (name[1], name[2], name[3], name[4], name[5], name[6], lat, lng, now_time)
            cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            error.append(names)
            print(e)
        n += 1
        if n == 3000 or n == 10000:
            print('进入等待60秒...')
            time.sleep(60)

if __name__ == '__main__':
    run()
    conn.close()
