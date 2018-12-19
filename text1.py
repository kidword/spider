import requests
import re
import json
import random

url = 'https://www.flightradar24.com/data/airports/BST/routes'
headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           ]

response = requests.get(url=url, headers={'User-Agent': random.choice(headers)}, verify=False)
# 得到了html 页面
html = response.text

# L = re.match(r'^[*]$',html)
L = re.search('arrRoutes=\[(.*?)\]', html,re.S).group(1)
ss = re.findall('{.*?}', L)
for j in ss:
    l = json.loads(j)
    print(l)
# print(type(L))
# S = eval(L)
# print(type(S))
# N = list(S)
# print(N)
# print(type(N))
# 得到一个字典类型








