#新加坡机场url
import requests
import re
import pandas as pd

url = 'https://www.flightradar24.com/data/airports/sin/routes'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
response = requests.get(url=url, headers=headers, verify=False)
html = response.text

L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)

#将 L转换成字典格式
tup = eval(L)
dic = list(tup)
n = 0
ll = []
#获取需要数据
for j in dic:
    n+=1
    # 获取到达机场代码
    flg_code = j['iata']
    # 获取到达机场名称
    # flg_name = j['name']
    # 获取到达机场经度
    flg_jingdu = j['lat']
    # 获取到达机场纬度
    flg_weidu = j['lon']
    list1 = ['SIN', flg_code, flg_jingdu, flg_weidu]
    ll.append(list1)
    #print(list1)
    #print('打印次数：', n, '起飞机场代码：','SIN' , '到达机场代码：', flg_code, '到达机场经度：', flg_jingdu, '到达机场纬度：',flg_weidu)

#写入csv文件中
name = ['F_code','A_code','ar_lat','ar_lon']
test = pd.DataFrame(columns=name,data=ll)
test.to_csv('D:\新加坡机场连接数据.csv')