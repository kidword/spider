import requests
import pymysql as py
import random
from lxml import etree

headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko)"
           " Version/5.1 Mobile/9A334 Safari/7534.48.3",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko)"
           " Chrome/20.0.1132.57 Safari/536.11",
           "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           ]

db = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = db.cursor()


# 获取国家名称
def getname():
    url = 'https://www.flightradar24.com/data/airports'
    timeout = random.choice(range(120, 180))
    response = requests.get(url=url, headers={'User-Agent': random.choice(headers)}, timeout=timeout)
    html = response.text
    select = etree.HTML(html)
    counrty = select.xpath('//*[@id="tbl-datatable"]/tbody/tr/td[3]/a/text()')
    return counrty
country = getname()


# 根据国家名称得到urls
def getdata():
    list = []
    for i in country:
        L = i.replace("'", "")
        L1 = L.replace("(", "")
        L2 = L1.replace(")", "")
        L3 = L2.replace(",", "")
        L4 = L3.strip()
        L5 = L4.replace(" ", "-")
        list.append(L5)
    return list


# 发起请求解析页面
def parse():
    url = 'https://www.flightradar24.com/data/airports/{}'
    print("国家数量：", len(getdata()))
    for name in getdata():
        try:
            urls = url.format(name)
            timeout = random.choice(range(90, 120))
            response = requests.get(url=urls, headers={'User-Agent': random.choice(headers)}, timeout=timeout)
            html = response.text
            select = etree.HTML(html)
            airports = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@title")
            code = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-iata")
            lat = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-lat")
            lon = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-lon")
            num = zip(airports, code, lat, lon)
            for j in num:
                sql = "insert into test_copy(Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon)" \
                      " values(%s,%s,%s,%s,%s)"
                param = (name, j[0], j[1], j[2], j[3])
                cursor.execute(sql, param)
                db.commit()
                print(name, j[0], j[1], j[2], j[3])
                print("----------------分割线-------------------")
        except requests.exceptions.ReadTimeout:
            print("发起请求超时")
        except requests.exceptions.ConnectionError:
            print("请求发生错误")


# 删除重复数据
def data():
    drop_sql = "DELETE from test_copy WHERE (Countries,Airports_name,Airports_code) in " \
               "(SELECT Countries,Airports_name,Airports_code from " \
               "(SELECT Countries,Airports_name,Airports_code FROM test_copy " \
               "GROUP BY Countries,Airports_name,Airports_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
               "(SELECT id from " \
               "(SELECT id FROM test_copy  GROUP BY Countries,Airports_name,Airports_code HAVING COUNT(*)>1) s2)"
    cursor.execute(drop_sql)
    db.commit()


if __name__ == '__main__':
    parse()
    data()
    db.close()

'''得到所有国家机场数据'''
