import requests
from bs4 import BeautifulSoup
import random
import pymysql as py


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


def lianjie():
    conn = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
    return conn
conn = lianjie()


def parse(url,qu):
    response = requests.get(url, headers={'User-Agent': random.choice(headers)})
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    next = soup.find('div', attrs={'class': 'page-box house-lst-page-box'}).get('page-data')
    data = eval(next)['totalPage']
    page = int(data)
    for u in range(1,page+1):
        urls = url + str(u)
        req = requests.get(url=urls, headers={'User-Agent': random.choice(headers)})
        html = BeautifulSoup(req.text, 'lxml')
        div = soup.select('div[class="houseInfo"]')
        for n in div:
            name = n.select('a')[0].get_text()
            huxing = n.select(".divide")[0].next_sibling
            mianji = n.select('.divide')[1].next_sibling
            chaoxiang = n.select('.divide')[2].next_sibling
            zhuangxiu = n.select('.divide')[3].next_sibling
            dianti = n.select('.divide')[4].next_sibling
            con = conn.cursor()
            sql = "insert into zufang_copy_copy(qu,name,huxing,mianji,chaoxiang,zhuangxiu,dianti) values(%s,%s,%s,%s,%s,%s,%s)"
            params = (qu,name,huxing,mianji,chaoxiang,zhuangxiu,dianti)
            con.execute(sql, params)
            conn.commit()
        div_price = soup.select('div[class="priceInfo"]')
        for pirce in div_price:
            m = pirce.select('span')[0].get_text()
            d = pirce.select('span')[1].get_text()
            con = conn.cursor()
            sql = "insert into zufang_copy_copy(zongjia,danjia) values(%s,%s)"
            params = (m,d)
            con.execute(sql, params)
            conn.commit()

if __name__ == '__main__':
    parse()
