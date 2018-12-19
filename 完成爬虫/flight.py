import pymysql as py
import requests
import json
import re
import time
import random

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 2018-07-26 14:55:07

headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
           ' Chrome/63.0.3239.132 Safari/537.36',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko)"
           " Chrome/20.0.1132.57 Safari/536.11",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           ]


# 代理ip使用
def pro():
    rd = open(r"D:/Users/dell/PycharmProjects/PY/IP_proxy/ip_proxy.txt")
    data = rd.read().split("\n")
    pro = []
    if len(data[0])>0:
        for i in data:
            if len(i)>1:
                pro.append(i)
    else:
        pro.append("http:121.31.150.47:8123")
    rd.close()
    return pro


# getConnection函数：连接数据库
def getconnection():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

# 加载数据库中数据
conn = getconnection()
cur = conn.cursor()
cn = cur.execute('select Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon from world')
rows = cur.fetchall()
rows = list(rows)
url = 'https://www.flightradar24.com/data/airports/{}/routes'
Airports_code1 = []
for i in rows:
    Airports_code1.append(list(i))
None_info_Airport = []  # 没有航班信息的机场代码


# 得到机场详细信息
def getinfo():
    for i in Airports_code1:
        try:
            urls = url.format(i[2])
            timeout = random.choice(range(30, 50))
            response = requests.get(url=urls, headers={'User-Agent': random.choice(headers)}, verify=True,
                                    timeout=timeout)
            html = response.text
            L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
            ss = re.findall('{.*?}', L)
            for j in ss:
                l = json.loads(j)
                flg_code = l['iata']  # 机场代码
                flg_name = l['name']  # 机场名称
                flg_city = l['city']  # 机场所在城市
                flg_country = l['country']  # 机场所在国家
                flg_lat = l['lat']  # 机场的经度
                flg_lon = l['lon']  # 机场的纬度
                sql_insert = "insert into flight_xin_copy" \
                             "(Take_off_airport_country,Take_off_airport_name,Take_off_airport_code," \
                             "Take_off_airport_alt,Take_off_airport_lon,Landing_airport_country,Landing_airport_name," \
                             "Landing_airport_code,Landing_airport_city,Landing_lat,Landing_lon) " \
                             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (i[0], i[1], i[2], i[3], i[4], flg_country, flg_name, flg_code, flg_city, flg_lat, flg_lon)
                cur.execute(sql_insert, param)
                conn.commit()
                print(i[0], i[1], i[2], i[3], i[4], flg_country, flg_name, flg_code, flg_city, flg_lat, flg_lon)
        except AttributeError:
            l = [i[0], i[1], i[2], i[3], i[4]]
            None_info_Airport.append(l)
            print('没有航线信息的机场：', i[2])
        except requests.exceptions.ReadTimeout:
            print('请求timeout超时',i)
        except requests.exceptions.ConnectionError:
            print("请求错误",i)


# 去重数据库中重复的数据
def data():
    try:
        print("执行sql语句")
        sql = "DELETE from flight_xin_copy WHERE (Take_off_airport_code,Landing_airport_code) in " \
              "(SELECT Take_off_airport_code,Landing_airport_code from " \
              "(SELECT Take_off_airport_code,Landing_airport_code FROM flight_xin_copy GROUP BY " \
              "Take_off_airport_code,Landing_airport_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
              "(SELECT id from (SELECT id FROM flight_xin_copy GROUP BY Take_off_airport_code,Landing_airport_code " \
              "HAVING COUNT(*)>1) s2);"
        cur.execute(sql)
        conn.commit()
    except:
        print('删除重复数据发生错误')

if __name__ == '__main__':
    getinfo()
    data()
    conn.close()

'''得到世界机场航线信息'''


