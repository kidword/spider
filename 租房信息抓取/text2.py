import requests
import threading
from bs4 import BeautifulSoup
import random

headers = [
           'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
           ' Chrome/63.0.3239.132 Safari/537.36']

pro = ['http:121.31.150.47:8123', 'http:220.184.215.248:6666']


def parse(url, qu):
    # 必须要通过解析得到页码数
    new = url+str(1)
    htm = requests.get(url, headers={'User-Agent': random.choice(headers)})
    soup = BeautifulSoup(htm.text, 'lxml')
    try:
        next = soup.find('div',attrs={'class':'page-box house-lst-page-box'}).get('page-data')
        data = eval(next)['totalPage']
        page = int(data)
    except:
        print('未解析出page页码数')
    for u in range(1, page+1):
        urls = url+str(u)
        req = requests.get(url = urls,headers={'User-Agent':random.choice(headers)}, proxies={'http':random.choice(pro)})
        html = BeautifulSoup(req.text, 'lxml')
        try:
            result = html.select('div[class="info-panel"]')
        except:
            print('未解析出对应div')
        for site in result:
            try:
                name = site.select('span')[0].get_text() #名称
                area = site.select('.con a')[0].get_text()
                louceng = site.select('.con span')[0].next_sibling
                huxing = site.select('span')[1].get_text()  # 户型
                mianji = site.select('.meters')[0].get_text() # 面积
                chaoxiang = site.select('span')[4].get_text() # 朝向
                price = site.select('.price span')[0].get_text() # 价格
                data = site.select('.price-pre')[0].get_text() # 发布时间
                print(name,area,louceng, huxing, mianji,chaoxiang,price,data)
            except:
                print('未解析出对应div下面元素')


# 创建新线程
thread1 = threading.Thread(target=parse, args=('https://bj.lianjia.com/zufang/chaoyang/pg', '东城区'))

thread1.start()

print("Exiting Main Thread")


