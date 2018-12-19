import pymysql as py
import requests
import json
import re
import time
import random

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 2018-07-26 14:55:07

headers = [ "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
    ]

# 代理ip使用
pro = ['http:118.190.95.35:9001', 'http:123.180.69.45:8010']


# getConnection函数：连接数据库
def getconnection():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

# 加载数据库中数据
conn = getconnection()
cur = conn.cursor()
info = []


# 数据库查询国家的全部信息，存到info列表中
def data():
    sql = "select * from world where countries='china'"
    cn = cur.execute(sql)
    rows = cur.fetchall()
    info.append(rows)


# 数据整理
def get():
    num = []  # 保存国家所有机场信息列表
    for i in info:
        for j in i:
            l = list(j)[1:]
            num.append(l)
    return num


def parse():
    url = 'https://www.flightradar24.com/data/airports/{}/routes'
    for code in get():
        try:
            urls = url.format(code[2])
            try:
                timeout = random.choice(range(80, 90))
                response = requests.get(url=urls, headers={'User-Agent': random.choice(headers)}, verify=True,
                                        timeout=timeout)
            except requests.exceptions.ConnectionError:
                print("请求超时")
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
                print("起飞国家：", code[0], "起飞机场：", code[1], "起飞代码：", code[2], "起飞经度：", code[3], "起飞纬度:", code[4],
                      "降落机场代码：", flg_code, "降落机场名称：", flg_name, "降落机场城市：", flg_city, "降落国家：", flg_country,
                      "降落经度：", flg_lat, "降落纬度：", flg_lon)
                sql_insert = "insert into china" \
                             "(Take_country,Take_airport,Take_code," \
                             "Take_alt,Take_lon,Landing_country,Landing_airport," \
                             "Landing_code,Landing_city,Landing_lat,Landing_lon) " \
                             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    param = (code[0], code[1], code[2], code[3], code[4], flg_country, flg_name,
                             flg_code, flg_city, flg_lat, flg_lon)
                    cur.execute(sql_insert, param)
                    conn.commit()
                except:
                    conn.rollback()
        except AttributeError:
            l = [code[0], code[1], code[2], code[3], code[4]]
            print("没有航班的机场代码：", code[2])
        except requests.exceptions.ReadTimeout:
            print('请求超时')


# 去重china表中爬取的重复数据
def drop_china():
    try:
        sql = "DELETE from china WHERE (Take_code,Landing_code) in " \
              "(SELECT Take_code,Landing_code from " \
              "(SELECT Take_code,Landing_code FROM ydyl GROUP BY " \
              "Take_code,Landing_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
              "(SELECT id from (SELECT id FROM ydyl GROUP BY Take_code,Landing_code " \
              "HAVING COUNT(*)>1) s2);"
        cur.execute(sql)
        conn.commit()
        print("开始执行drop_china方法")
    except:
        print('删除重复数据发生错误')


# 从china表中查出需要数据插入ydyl表中
def select_china():
    try:
        sql = 'insert into ydyl_copy (Take_country,Take_airport,Take_code,Take_alt,Take_lon,Landing_country,' \
              'Landing_airport,' \
              'Landing_code,Landing_city,Landing_lat,Landing_lon) select Take_country,Take_airport,Take_code,Take_alt,' \
              'Take_lon,Landing_country,Landing_airport,Landing_code,Landing_city,Landing_lat,Landing_lon ' \
              'from china where Take_country="China" and Landing_country in ("Bhutan","Ukraine","Uzbekistan",' \
              '"yemen","Armenia","israel","Iraq","Iran","Russia","Bulgaria","Croatia","Hungary","qatar","India",' \
              '"indonesia","Syria","kyrgyzstan","Kazakhstan","turkmenistan","Turkey","egypt","tajikistan","Serbia",' \
              '"cyprus","Bangladesh","Nepal","Pakistan","sudan","Bahrain","greece","Latvia","czech-republic","moldova",' \
              '"Brunei","Slovakia","Slovenia","sri-lanka","Singapore","cambodia","Georgia","saudi-arabia","Poland",' \
              '"bosnia-and-herzegovina","Thailand","Armenia","belarus","kuwait","Lithuania","Jordan","myanmar-burma",' \
              '"Romania","Laos","Philippines","Mongolia","Vietnam","azerbaijan","Afghanistan","Albania","oman",' \
              '"united-arab-emirates","Macedonia","Maldives","malaysia","Lebanon","Montenegro")'
        cur.execute(sql)
        conn.commit()
        print("开始执行select_china方法")
    except:
        print('插入数据错误')


# 去除一带一路数据表中的重复数据
def drop_ydyl():
    try:
        sql = "DELETE from ydyl_copy WHERE (Take_code,Landing_code) in " \
              "(SELECT Take_code,Landing_code from " \
              "(SELECT Take_code,Landing_code FROM ydyl_copy GROUP BY " \
              "Take_code,Landing_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
              "(SELECT id from (SELECT id FROM ydyl_copy GROUP BY Take_code,Landing_code " \
              "HAVING COUNT(*)>1) s2);"
        cur.execute(sql)
        conn.commit()
        print("开始执行drop_ydyl方法")
    except:
        print('数据去重错误')

if __name__ == '__main__':
    data()
    parse()
    drop_china()
    # 以下是mysql数据库的数据处理
    select_china()
    drop_ydyl()
    conn.close()

'''得到一带一路国家中，中国机场飞往一代一路国家机场数据信息'''
