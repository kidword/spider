import requests
import re
import json
url = 'https://www.flightradar24.com/data/airports/BST/routes'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
response = requests.get(url=url, headers=headers,verify=True)

html = response.text
L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
ss = re.findall('{.*?}', L)
for i in ss:
    l = json.loads(i)
    print(l)
    print(type(l))
# l = json.loads(L)
# print(l)
# 将正则匹配出的数据转换成字典类型
# l = eval(L)
# lis = list(l)
#
# for i in lis:
#     print(i)
# dic = json.loads(L)
# print(type(dic))
# print(dic)
