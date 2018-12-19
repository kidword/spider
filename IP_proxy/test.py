import requests
import datetime
from lxml import etree
from threading import Thread
from queue import Queue
from user_agents import agents
import random
from lxml import etree


class QiushiSpider:
    def __init__(self):
        self.url = 'https://www.flightradar24.com/data/airports'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        self.urls = 'https://www.flightradar24.com/data/airports/{}'
        self.url_q = Queue()  # url队列
        self.html_q = Queue()  # 响应内容队列
        self.item_q = Queue()  # 提取的数据结果队列

    def makeUrlList(self):
        """构造url_list并添加队列"""
        timeout = random.choice(range(120, 180))
        response = requests.get(self.url, headers={'User-Agent': random.choice(agents)}, timeout=timeout)
        ht = response.text
        select = etree.HTML(ht)
        counrty = select.xpath('//*[@id="tbl-datatable"]/tbody/tr/td[3]/a/text()')
        list1 = []
        for i in counrty:
            L = i.replace("'", "")
            L1 = L.replace("(", "")
            L2 = L1.replace(")", "")
            L3 = L2.replace(",", "")
            L4 = L3.strip()
            L5 = L4.replace(" ", "-")
            list1.append(L5)
        print(list1)
        for j in list1:
            self.url_q.put(self.urls.format(j))

    def getHtml(self):
        """发送请求获取响应,并添加队列"""
        while True:
            url = self.url_q.get()
            resp = requests.get(url, headers=self.headers)
            self.html_q.put(resp.text)
            self.url_q.task_done()  # 让url_q计数-1

    def parseItem(self):
        """提取数据(先分组,再提取),并添加队列"""
        while True:
            print("进入解析方法中")
            html_str = self.html_q.get()
            html = etree.HTML(html_str)
            result_list = []
            item = {}
            item['name'] = html.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@title")  # 用户昵称
            item['content'] = html.xpath("//*[@id='tbl-datatable']/tbody/tr/td[2]/a/@data-iata")  # 内容提要
            result_list.append(item)
            self.item_q.put(result_list)
            self.html_q.task_done()  # 计数-1

    def excuteItem(self):
        """处理或保存结果列表中的每一条数据"""
        while True:
            result_list = self.item_q.get()
            for item in result_list:
                print(item)
            self.item_q.task_done()  # 计数-1

    def run(self):
        """逻辑"""
        # 构造url_list
        self.makeUrlList()

        t_list = []  # 构造一个存放所有线程对象的列表
        # 发送请求获取响应,并返回响应内容
        for i in range(3):  # 开启三个发送请求的线程,来提高发送请求的效率
            t_parse = Thread(target=self.getHtml)
            t_list.append(t_parse)
        # 解析数据
        for i in range(2):
            t_content = Thread(target=self.parseItem)
            t_list.append(t_content)
        # 处理或保存
        t_save = Thread(target=self.excuteItem)
        t_list.append(t_save)

        for t in t_list:
            t.setDaemon(True)  # 设置线程为守护线程:主线程结束,子线程跟着一起结束
            t.start()

        for q in [self.url_q, self.html_q, self.item_q]:
            q.join()  # 让每个q队列阻塞主线程
            # 每个q队列的计数为0的时候,才停止阻塞

        print('程序结束了')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    spider = QiushiSpider()
    spider.run()
    end_time = datetime.datetime.now()
    print(end_time-start_time)
