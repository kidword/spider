import requests
import re
import json
import pandas as pd

lis_name= ['BDP', 'BHR', 'BIR', 'JKR', 'JMO', 'KTM', 'LUA', 'KEP', 'PPL', 'PKR', 'BWA', 'TMI']
n = 0
e_error = 0
ll = []
#错误机场代码
error_code = []
#未来7天没有飞机起飞的机场代码
none_code = []

#null nameError
N_code = []
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
        ER_fl = ['BDP', 'JKR', 'JMO', 'LUA', 'PPL']
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
        ER_f2 = ['GAU', 'CCU', 'IXS']
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
        print('起飞机场代码：', i, '{}此机场未来7天没有航信信息'.format(i))
    except TypeError:
        error_code.append(i)
        print('错误机场代码：',i)

    except NameError:
        e_error +=1
        N_code.append(i)
        print('错误次数：',e_error,)
print('--------------------------------------分割线--------------------------------------------')

print('未来7天没有航线机场：',none_code)
print('错误机场代码，需要重新解析：',error_code)
print('出现格式解析错误，需要重新解析：',N_code)

#写入csv文件中
name = ['F_code(起飞机场)', 'A_code（到达机场）', 'ar_lat（经度）', 'ar_lon（纬度）']
test = pd.DataFrame(columns=name,data=ll)
test.to_csv('D:\尼泊尔机场连接数据.csv')