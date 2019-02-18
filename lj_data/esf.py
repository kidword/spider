import requests
import threading
from bs4 import BeautifulSoup
import random
import pymysql as py
import re
import datetime

headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
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
# pro = ['http:121.31.150.47:8123','http:220.184.215.248:6666']


def lianjie():
    conn = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
    return conn


conn = lianjie()


def parse(url, qu):
    # 必须要通过解析得到页码数
    global name, huxing, mianji, chaoxiang, price, data, area, louceng, page, result
    timeout = random.choice(range(120, 180))
    new = url + str(1)
    htm = requests.get(url, headers={'User-Agent': random.choice(headers)}, timeout=timeout)
    soup = BeautifulSoup(htm.text, 'lxml')
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        next = soup.find('div', attrs={'class': 'page-box house-lst-page-box'}).get('page-data')
        data = eval(next)['totalPage']
        page = int(data)
    except:
        print('未解析出page页码数')
    for u in range(1, page + 1):
        urls = url + str(u)
        req = requests.get(url=urls, headers={'User-Agent': random.choice(headers)}, timeout=timeout)
        html = BeautifulSoup(req.text, 'lxml')
        div_l = html.select('div[class="houseInfo"]')
        price = html.select('div[class="priceInfo"]')
        apartment = []
        area = []
        address = []
        s_price = []
        g_price = []
        for d in div_l:
            name = d.select("a")[0].get_text()
            apart = d.select('span')[0].next_sibling
            are = d.select('span')[1].next_sibling.replace("平米",'')
            address.append(name)
            apartment.append(apart)
            area.append(are)
            for p in price:
                z_price = p.select('div[class="totalPrice"] span')[0].get_text()
                d_price = p.select('div[class="unitPrice"] span')[0].get_text()
                num = re.findall('\d+', d_price)
                s_price.append(z_price)
                g_price.append(num)
        new_data = zip(address, area, apartment, s_price, g_price)
        for d in new_data:
            item = dict()
            item['address'] = d[0]
            item['area'] = d[1]
            item['apartment'] = d[2]
            item['d_price'] = d[3]
            item['z_price'] = d[4]
            item['qu'] = qu
            print(item)
            try:
                con = conn.cursor()
                sql = "insert into lj_spider(qu,address,apartment,area,d_price,z_price,dtime) values(%s,%s,%s,%s,%s,%s,%s)"
                params = (item['qu'], item['address'], item['apartment'], item['area'], item['d_price'], item['z_price'], now_time)
                con.execute(sql, params)
                conn.commit()
            except Exception as e:
                print('数据库连接错误，请检查数据......', e)


# 删除zufang_copy重复数据
def drop_data():
    print("执行删除重复数据...")
    con = conn.cursor()
    drop_sql = "DELETE from lj_spider WHERE (address, apartment,area,dtime) in " \
               "(SELECT address, apartment,area,dtime from " \
               "(SELECT address, apartment,area,dtime FROM lj_spider " \
               "GROUP BY address, apartment,area,dtime HAVING COUNT(*)>1) s1) AND  id NOT in " \
               "(SELECT id from (SELECT id FROM lj_spider " \
               "GROUP BY address, apartment,area,dtime HAVING COUNT(*)>1) s2)"
    con.execute(drop_sql)
    conn.commit()
    print("删除完成...")


# 创建新线程
thread1 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/dongcheng/pg', '东城区'))
thread2 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/xicheng/pg', '西城区'))
thread3 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/chaoyang/pg', '朝阳区'))
thread4 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/haidian/pg', '海淀区'))
thread5 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/fengtai/pg', '丰台区'))
thread6 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/shijingshan/pg', '石景山区'))
thread7 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/tongzhou/pg', '通州区'))
thread8 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/changping/pg', '昌平区'))
thread9 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/daxing/pg', '大兴区'))
thread10 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/shunyi/pg', '顺义区'))
thread11 = threading.Thread(target=parse, args=('https://bj.lianjia.com/ershoufang/fangshan/pg', '房山区'))

# 开启线程
if __name__ == '__main__':
    threads = [thread1, thread2, thread3, thread4, thread5, thread6,
               thread7, thread8, thread9, thread10, thread11]
    for t in threads:
        t.start()
        t.join()
    drop_data()
    # 关闭数据库连接
    conn.close()
'''链家租房数据'''

