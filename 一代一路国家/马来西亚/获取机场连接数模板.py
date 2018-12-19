import requests
import re
import pandas as pd

lis_name=['AOR', 'BKM', 'BBN', 'BTU', 'IPH', 'JHB', 'KTE', 'KBR', 'BKI', 'KUL', 'SZB', 'TGG', 'KUA', 'KCH', 'KUD', 'LBU', 'LDU', 'LGK', 'LWY', 'LMN', 'LKH', 'LGL', 'MKZ', 'MUR', 'MYY', 'MKM', 'MZV', 'PEN', 'SDK', 'SBW', 'TGC', 'TWU']
n = 0
ll = []
for i in lis_name:
        n += 1
        url = 'https://www.flightradar24.com/data/airports/{}/routes'
        new_url = url.format(i)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        response = requests.get(url=new_url, headers=headers,verify=False)
        html = response.text
        L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
        # ER_fl出现错误的一些机场代码
        ER_fl = ['KTE','LDU']
        if i in ER_fl:
            S = eval(L)
        else:
            S = eval(L)
            dic = list(S)
        for j in dic:
            # 获取到达机场代码
            flg_code = j['iata']
            # 获取到达机场名称
            # flg_name = j['name']
            # 获取到达机场经度
            flg_jingdu = j['lat']
            # 获取到达机场纬度
            flg_weidu = j['lon']
            list1 = [i, flg_code, flg_jingdu, flg_weidu]
            ll.append(list1)
            #print('打印次数：', n, '起飞机场代码：', i, '到达机场代码：', flg_code, '到达机场经度：', flg_jingdu, '到达机场纬度：', flg_weidu)

#写入csv文件中
name = ['F_code(起飞机场)', 'A_code（到达机场）', 'ar_lat（经度）', 'ar_lon（纬度）']
test = pd.DataFrame(columns=name,data=ll)
test.to_csv('D:\马来西亚机场连接数据.csv')