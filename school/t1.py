from urllib import parse
import urllib.request
import json
import pymysql as py


# 读取数据库数据
def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

conn = getmysql()
cur = conn.cursor()
cn = cur.execute('select * from ydyl_university')
rows = cur.fetchall()
rows = list(rows)


def getname():
    name_lis = []
    for lis in rows:
        name_lis.append(list(lis))
    return name_lis
l = getname()
print(l)
error = []

#
def getarea():
    n = 1
    for name in l:
        names = name[1]
        query = {
          'key': 'f247cdb592eb43ebac6ccd27f796e2d2',
          'address': names,
          'output': 'json',
           }
        base = 'http://api.map.baidu.com/geocoder?'
        url = base+parse.urlencode(query)
        doc = urllib.request.urlopen(url)
        s = doc.read().decode('utf-8')  # 一定要解码！！！！
        jsonData = json.loads(s)
        try:
            lat = jsonData['result']['location']['lat']
            lng = jsonData['result']['location']['lng']
            print(name[1], name[2], lng, lat)
            cur = conn.cursor()
            sql = "insert into ydyl_school(country,school,alt,lon) " \
                  "values(%s,%s,%s,%s)"
            params = (name[0], name[1], lat, lng)
            cur.execute(sql, params)
            conn.commit()
        except:
            error.append(names)

getarea()

print("error错误信息：",error)