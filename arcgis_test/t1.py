import requests
from user_agents import agents
import random
from lxml import etree
import threading


# 执行1  得到html
def get_html(url):
    por = ["113.13.29.63:8118", "222.181.10.243:8118"]
    response = requests.get(
        url=url,
        headers={"User-Agent": random.choice(agents)},
        proxies={'http': random.choice(por)}
    )
    # print(response.text)
    html = response.text
    get_proxy(html)


# 执行2 解析html
def get_proxy(html):
    selector = etree.HTML(html)
    name = selector.xpath()
    lis = []
    test_proxies(lis)
    # 从html中解析出来的数据添加到lis中


# 执行3 测试数据是否正常
def test_proxies(lis):
    lis = lis  # 接收数据
    # 下面对lis数据进行遍历，开启多线程
    for proxy in lis:
        test = threading.Thread(target=thread_test_proxy, args=(proxy,))
        test.start()


# 执行4 对数据进行测试
def thread_test_proxy(lis):
    url = ''
    lis= ''
    thread_write_proxy(lis)


# 执行5 对数据进行写入：
def thread_write_proxy(lis):
    with open(r"D:\test.txt") as f:
        print("正在写入",lis)
        f.write(lis + '\n')
        print("录入完成！！！")


if __name__ == '__main__':
    # 得到所有url
    for i in range(1, 3):
        url = "http://www.xicidaili.com/nn/" + str(i)
        get_html(url)
