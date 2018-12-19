import requests
import threading
from bs4 import BeautifulSoup
import lxml
from lxml import etree
import random
import pymysql as py
import time
import datetime

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

# 代理池
pro = ['http:121.31.150.47:8123','http:220.184.215.248:6666']
def lianjie():
    conn = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
    return conn
conn = lianjie()


def parse(url,num,qu):
    for i in range(1,num):
        ls = url.format(i)
        print(ls)
        response = requests.get(ls, headers={'User-Agent': random.choice(headers)},proxies={'http':random.choice(pro)})
        time.sleep(1)
        html = response.text
        xp = etree.HTML(html)
        title = xp.xpath('/html/body/div[4]/div[1]/div[2]/ul/li/div[2]/div[1]/p[1]/text()')
        area = xp.xpath('/html/body/div[4]/div[1]/div[2]/ul/li/div[2]/div[1]/p[2]/a/text()')
        d_price = xp.xpath('/html/body/div[4]/div[1]/div[2]/ul/li/div[2]/div[1]/div/p[2]/text()')
        z_price = xp.xpath('/html/body/div[4]/div[1]/div[2]/ul/li/div[2]/div[1]/div/p[1]/strong/text()')
        huxing_lis = []
        mianji_lis = []
        chaoxiang_lis = []
        louceng_lis = []
        zhuangxiu_lis = []
        for t in title:
            team = str(t)
            l = team.split('·')
            huxing_lis.append(l[0])
            mianji_lis.append(l[1])
            chaoxiang_lis.append(l[2])
            louceng_lis.append(l[3])
         # 解析html
        mesg = zip(area,huxing_lis,mianji_lis,chaoxiang_lis,louceng_lis,d_price,z_price)
        for ms in mesg:
            list1 = list(ms)
            print(list1)
            con = conn.cursor()
            sql = "insert into er_shoufang_copy(Qu,Er_name,Price,Dan_Price,Hu_Xing,Mian_ji,LouCeng,ChaoXiang) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            params = (qu,list1[0],list1[6],list1[5],list1[1],list1[2],list1[4],list1[3])
            con.execute(sql, params)
            conn.commit()

# 创建新线程
thread1 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/chaoyangqu/n{}',216,'朝阳区'))
thread2 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/haidianqu/n{}',128,'海淀区'))
thread3 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/donchengqu/n{}',37,'东城区'))
thread4 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/xichengqu/n{}',71,'西城区'))
thread5 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/fengtaiqu/n{}',95,'丰台区'))
thread6 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/shijingshanqu/n{}',20,'石景山区'))
thread7 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/tongzhouqu/n{}',98,'通州区'))
thread8 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/changpingqu/n{}',80,'昌平区'))
thread9 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/daxingqu/n{}',55,'大兴区'))
thread10 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/shunyiqu/n{}',41,'顺义区'))
thread11 = threading.Thread(target=parse,args=('https://bj.5i5j.com/ershoufang/fangshanqu/n{}',33,'房山区'))

if __name__ == '__main__':
    threads = [thread1,thread2,thread3,thread4,thread5,thread6,thread7,thread8,thread9,thread10,thread11]
    for t in threads:
        t.start()
        time.sleep(1)
        t.join()
    conn.close() # 关闭数据库连接





