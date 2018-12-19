from selenium import webdriver
import pymysql as py
import re
import json
import requests
pj = webdriver.PhantomJS()

url = "http://www.flightradar24.com/data/airports/{}/routes"


def getconnection():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

conn = getconnection()
cur = conn.cursor()
cn = cur.execute('select Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon from world')
rows = cur.fetchall()
rows = list(rows)

Airports_code1 = []
for i in rows:
    Airports_code1.append(list(i))
None_info_Airport = []  # 没有航班信息的机场代码


def getinfo():
    for i in Airports_code1:
        try:

            urls = url.format(i[2])
            pj.get(urls)
            html = pj.page_source
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
            print('请求timeout超时')
        except requests.exceptions.ConnectionError:
            print("请求错误")
getinfo()
