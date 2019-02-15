from urllib import parse
import pymysql as py
from queue import Queue
import requests
from threading import Thread
from fake_useragent import UserAgent
import json
import datetime
import random
import time

Today = datetime.datetime.now()  # 获取当天时间
Today1 = Today.strftime('%Y-%m-%d')
ua = UserAgent()


class Mysql:
    def __init__(self):
        self.password = 'hh226752'
        self.db = 'flightradar24'
        self.user = 'root'

    def mysql_connection(self):
        db = py.connect(host='localhost', user=self.user, passwd=self.password,
                        db=self.db, charset='utf8')
        return db

    @classmethod
    def insert(cls):
        sql = "insert into lj_xb(qu,address,apartment,area,d_price,z_price,lat,lon,dtime)" \
              " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        return sql

    def close_mysql(self):
        db = self.mysql_connection()
        db.close()


class LianJia(Mysql):
    def __init__(self):
        super(LianJia, self).__init__()
        self.url_q = Queue()
        self.html_q = Queue()
        self.item_q = Queue()

    def getmysql(self):
        conn = py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')
        cur = conn.cursor()
        cn = cur.execute('select * from lj_spider where dtime="{}"'.format(Today1))
        rows = cur.fetchall()
        rows = list(rows)
        name_lis = []
        for lis in rows:
            name_lis.append(list(lis))
        return name_lis

    def make_url(self):
        urls = self.getmysql()
        for name in urls:
            dict1 = dict()
            names = name[1] + name[2]
            query = {
                'key': 'f247cdb592eb43ebac6ccd27f796e2d2',
                'address': names,
                'output': 'json',
            }
            base = 'http://api.map.baidu.com/geocoder?'
            url = base + parse.urlencode(query)
            dict1['qu'] = name[1]
            dict1['address'] = name[2]
            dict1['apartment'] = name[3]
            dict1['area'] = name[4]
            dict1['d_price'] = name[5]
            dict1['z_price'] = name[6]
            dict1['url'] = url
            self.url_q.put(dict1)

    def send_request(self):
        while True:
            dict1 = self.url_q.get()
            url = dict1['url']
            headers = {"User-Agent": ua.random}
            try:
                timeout = random.randrange(30, 40)
                resp = requests.get(url, headers=headers, timeout=timeout)
                if resp.status_code == 200:
                    dict1['html'] = resp.content.decode('utf-8')
                    self.html_q.put(dict1)
                    self.url_q.task_done()
                else:
                    break
            except Exception as e:
                print(e)

    def parseitem(self):
        while True:
            dict1 = self.html_q.get()
            html_str = dict1['html']
            result_list = []
            try:
                jsonData = json.loads(html_str)
                item = dict()
                item['qu'] = dict1['qu']
                item['address'] = dict1['address']
                item['apartment'] = dict1['apartment']
                item['area'] = dict1['area']
                item['d_price'] = dict1['d_price']
                item['z_price'] = dict1['z_price']
                item['lat'] = jsonData['result']['location']['lat']
                item['lng'] = jsonData['result']['location']['lng']
                print(item)
                result_list.append(item)
            except Exception as e:
                print(e)
            self.item_q.put(result_list)
            self.html_q.task_done()

    def handle_item(self):
        conn = self.mysql_connection()
        while True:
            result_list = self.item_q.get()
            for item in result_list:
                cur = conn.cursor()
                params = (item['qu'], item['address'], item['apartment'], item['area'],
                          item['d_price'], item['z_price'], item['lat'], item['lng'], Today1)
                cur.execute(self.insert(), params)
                conn.commit()

    def run(self):
        self.make_url()
        t_list = []
        for i in range(3):
            t_parse = Thread(target=self.send_request)
            t_list.append(t_parse)

        for i in range(2):
            t_content = Thread(target=self.parseitem)
            t_list.append(t_content)

        t_save = Thread(target=self.handle_item)
        t_list.append(t_save)

        for t in t_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_q, self.html_q, self.item_q]:
            q.join()
        print('爬取结束')


if __name__ == '__main__':
    spider = LianJia()
    spider.run()
    spider.close_mysql()
