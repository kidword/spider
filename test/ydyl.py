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
pro = ['http:121.31.150.47:8123', 'http:220.184.215.248:6666']


# getConnection函数：连接数据库
def getconnection():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

# 加载数据库中数据
conn = getconnection()
cur = conn.cursor()
# 一代一路65个国家名称
counrty = ["Bhutan","Ukraine","Uzbekistan","yemen","Armenia","israel","Iraq","Iran","Russia","Bulgaria","Croatia","Hungary","qatar"
            "India","indonesia","Syria","kyrgyzstan","Kazakhstan","turkmenistan","Turkey","egypt","tajikistan","Serbia","cyprus",
           "Bangladesh","Nepal","Pakistan","sudan","Bahrain","greece","Latvia","czech-republic","moldova","Brunei","Slovakia",
           "Slovenia","sri-lanka","Singapore","cambodia","Georgia","saudi-arabia","Poland","bosnia-and-herzegovina","Thailand","Armenia",
           "belarus","kuwait","Lithuania","Jordan","myanmar-burma","Romania","Laos","Philippines","Mongolia","Vietnam","azerbaijan",
           "Afghanistan","Albania","oman","united-arab-emirates","Macedonia","Maldives","malaysia","Lebanon","Montenegro","china"]

info = []


# 数据库查询国家的全部信息，存到info列表中
def data():
    for i in counrty:
        sql = "select * from test_copy where countries='{}'".format(i)
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
            timeout = random.choice(range(120, 180))
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
                print("起飞国家：", code[0], "起飞机场：", code[1], "起飞代码：", code[2], "起飞经度：", code[3], "起飞纬度:", code[4],
                      "降落机场代码：", flg_code, "降落机场名称：", flg_name, "降落机场城市：", flg_city, "降落国家：", flg_country,
                      "降落经度：", flg_lat, "降落纬度：", flg_lon)
                sql_insert = "insert into ydyl" \
                             "(Take_country,Take_airport,Take_code," \
                             "Take_alt,Take_lon,Landing_country,Landing_airport," \
                             "Landing_code,Landing_city,Landing_lat,Landing_lon) " \
                             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (code[0], code[1], code[2], code[3], code[4], flg_country, flg_name,
                         flg_code, flg_city, flg_lat, flg_lon)
                cur.execute(sql_insert, param)
                conn.commit()
        except AttributeError:
            l = [code[0], code[1], code[2], code[3], code[4]]
        except requests.exceptions.ReadTimeout:
            print('请求超时')

if __name__ == '__main__':
    data()
    parse()
    conn.close()
