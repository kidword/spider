import requests
import re
import pandas as pd
import json
lis_name= ['DMK', 'BKK', 'BFV', 'CNX', 'CEI', 'CJM', 'HDY', 'HHQ', 'KKC', 'USM', 'KBV', 'LPT', 'LOE', 'HGN', 'MAQ', 'KOP', 'NAK', 'NST', 'NNT', 'NAW', 'PHS', 'PRH', 'HKT', 'UNN', 'UTP', 'ROI', 'SNO', 'THS', 'URT', 'TST', 'TDX', 'UBP', 'UTH']
n = 0
ll = []
#错误机场代码
error_code = []
#未来7天没有飞机起飞的机场代码
none_code = []
for i in lis_name:
    try:
        n += 1
        url = 'https://www.flightradar24.com/data/airports/{}/routes'
        new_url = url.format(i)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        response = requests.get(url=new_url, headers=headers,verify=False)
        html = response.text
        L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
        # ER_fl出现错误的一些机场代码
        ER_fl = ['BFV', 'CJM', 'HHQ', 'LOE', 'MAQ', 'KOP', 'NST', 'NNT', 'PHS', 'PRH', 'UNN', 'ROI', 'SNO', 'THS', 'TST', 'TDX']
        if i in ER_fl:
            S = eval(L)
            flg_code = S['iata']
            # 获取到达机场名称
            # flg_name = j['name']
            # 获取到达机场经度
            flg_jingdu = S['lat']
            # 获取到达机场纬度
            flg_weidu = S['lon']
            list2 = [i, flg_code, flg_jingdu, flg_weidu]
            print(list2)
            error_code.append(i)
            ll.append(list2)
        ER_f2=['GAU', 'CCU', 'IXS']
        if i in ER_f2:
            ss = re.findall('{.*?}', L)
            for s in ss:
                # print(eval(s))
                l = json.loads(s)
                flg_code = l['iata']
                # 获取到达机场名称
                # flg_name = l['name']
                # 获取到达机场经度
                flg_jingdu = l['lat']
                # 获取到达机场纬度
                flg_weidu = l['lon']
                lis3 = [i, flg_code, flg_jingdu, flg_weidu]
                ll.append(lis3)
                print(lis3)
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
                print('打印次数：', n, '起飞机场代码：', i, '到达机场代码：', flg_code, '到达机场经度：', flg_jingdu, '到达机场纬度：', flg_weidu)
    except AttributeError:
        none_code.append(i)
        #print('起飞机场代码：', i, '{}此机场未来7天没有航信信息'.format(i))
    except TypeError:
        error_code.append(i)
        #print('错误机场代码：',i)
    # except NameError:
    #     pass
print('未来7天没有航班信息机场列表：',none_code)
print('错误机场代码：',error_code)
#写入csv文件中
name = ['F_code(起飞机场)', 'A_code（到达机场）', 'ar_lat（经度）', 'ar_lon（纬度）']
test = pd.DataFrame(columns=name,data=ll)
test.to_csv('D:\泰国机场连接数据.csv')