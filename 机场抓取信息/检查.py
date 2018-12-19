'''
将上周没有航班信息的机场数据在下周在爬取一遍
'''


import codecs
import pandas as pd
import csv
import requests
import re
import json
import pymysql as py


def readCSV2List(filePath):
    try:
        file=open(filePath,'r',encoding="gb18030")# 读取以utf-8
        context = file.read() # 读取成str
        list_result=context.split("\n")#  以回车符\n分割成单独的行
        #每一行的各个元素是以【,】分割的，因此可以
        length=len(list_result)
        for i in range(length):
            list_result[i]=list_result[i].split(",")
        return list_result
    except Exception :
        print("文件读取转换失败，请检查文件路径及文件编码是否正确")
    finally:
        file.close();# 操作完成一定要关闭
list1 = readCSV2List(r'D:\no.csv')
list3 = []
def flg_code():
    list2 = list1[1:-1]
    for i in list2:
        list3.append(i[2])
flg_code()

def getConnection():
    return py.connect(host='localhost', user='root', password='hh226752',db = 'flightradar24', charset = 'utf8' )

# 加载数据库中数据
conn = getConnection()
cur = conn.cursor()
cn = cur.execute('select * from test')

rows = cur.fetchall()
rows = list(rows)
airport_info = []
for i in rows:
   list1 =  list(i)
   airport_info.append(list1)
url = 'https://www.flightradar24.com/data/airports/{}/routes'
None_info_Airport=[]
to_csv = []
for i in list3:
    try:
        new_url = url.format(i)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        response = requests.get(url=new_url, headers=headers,verify=True)
        html = response.text
        L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
        ss = re.findall('{.*?}', L)
        for j in ss:
            l = json.loads(j)
            flg_code = l['iata'] # 机场代码
            flg_name = l['name'] # 机场名称
            flg_city = l['city'] # 机场所在城市
            flg_country = l['country'] # 机场所在国家
            flg_lat = l['lat'] # 机场的经度
            flg_lon = l['lon'] # 机场的纬度
            list2 = [i,flg_country,flg_name,flg_code,flg_city,flg_lat,flg_lon]
            to_csv.append(list2)
            print(flg_country,flg_code,flg_name,flg_city,flg_lat,flg_lon)
    except AttributeError:
        None_info_Airport.append(i)

        #print('没有航线信息的机场：',i)

# to_csv = []
# for i in airport_info:
#     for k in list3:
#         if k in i:
#             to_csv.append(i[1:])
# print(to_csv)
#
# 新增机场数据
name = ['起飞机场代码','国家名称','机场名称','机场代码','机场经度','机场纬度']
test = pd.DataFrame(columns=name, data=to_csv)
test.to_csv('D:\新增机场信息列表.csv')


# 得到一个list 以后， 通过list里面的每个元素 在主表中查找信息,然后写入新的csv 或者mysql 数据库中
# list 里面有499个数据， select * from test where airports_code = '?'
# 表名 test  列名airprots_code   list1 = []  通过 list1 中元素， 在airport_code 中查出全部信息来

