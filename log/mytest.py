import logging.config
import requests
import pymysql as py
import random
from lxml import etree

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("example01")

headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko)"
           " Version/5.1 Mobile/9A334 Safari/7534.48.3",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           ]
# 代理ip
pro = ['http:121.31.150.47:8123', 'http:220.184.215.248:6666']

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
    url_lis = []
    for i in country:
        L = i.replace("'", "")
        L1 = L.replace("(", "")
        L2 = L1.replace(")", "")
        L3 = L2.replace(",", "")
        L4 = L3.strip()
        L5 = L4.replace(" ", "-")
        list.append(L5)
    return url_lis


# 发起请求解析页面
def parse():
    try:
        url = 'https://www.flightradar24.com/data/airports/{}'
        print("国家数量：", len(getdata()))
        for name in getdata():
            urls = url.format(name)
            timeout = random.choice(range(120, 180))
            response = requests.get(url=urls, headers={'User-Agent': random.choice(headers)}, timeout=timeout,
                                    proxies={'http': random.choice(pro)})
            html = response.text
            select = etree.HTML(html)
            airports = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@title")
            code = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-iata")
            lat = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-lat")
            lon = select.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-lon")
            num = zip(airports, code, lat, lon)
            for j in num:
                sql = "insert into tes(Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon)" \
                      " values(%s,%s,%s,%s,%s)"
                param = (name, j[0], j[1], j[2], j[3])
                cursor.execute(sql, param)
                db.commit()
                print(name, j[0], j[1], j[2], j[3])
                print("----------------分割线-------------------")
    except:
        logging.error("There is a error in this file", exc_info=1)

parse()
