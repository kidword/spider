import requests
from lxml import etree
import random

headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
           " Chrome/63.0.3239.132 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) "
           "Chrome/20.0.1132.57 Safari/536.11",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           ]


def into():
    q_ulr = []
    name = []
    url = 'https://bj.5i5j.com/zufang/haidianqu/'
    html = requests.get(url, headers={'User-Agent': random.choice(headers)}).text
    selector = etree.HTML(html)
    href = selector.xpath('/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/dl/dd/span/a/@href')
    title = selector.xpath('/html/body/div[3]/div[2]/div/ul/li[1]/div[3]/div[1]/dl/dd/span/a/text()')
    data = zip(title, href)
    for i in data:
        urls = 'https://bj.5i5j.com'+str(i[1])
        q_ulr.append(urls)
        name.append(i[0])
        print(i[0])
    return q_ulr, name
into()


def parse():
    data = into()
    print(data)
    # url = list(data)

    # for j in data[1]:
    #     url = 'https://bj.5i5j.com'+str(j)
    #     print(url)
    #     ht = requests.get(url, headers={'User-Agent': random.choice(headers)}).text
    #     select = etree.HTML(ht)
    #     title = select.xpath("/html/body/div[4]/div[1]/div[2]/ul/li[1]/div[2]/div[1]/p[2]/a/text()")
    #     print(title)
parse()
