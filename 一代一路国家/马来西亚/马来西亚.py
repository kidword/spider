from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests
import re
import pandas as pd

browser=webdriver.Chrome()
browser.get("https://www.flightradar24.com/data/airports/malaysia")
lis=browser.find_elements_by_css_selector("#tbl-datatable > tbody > tr > td > a")

new_lis = []
for i in lis:
    # 获取机场名称
    flight_name = i.get_attribute('title')
    # 获取机场号码
    ph = i.get_attribute('data-iata')
    # 得到经度
    jindu = i.get_attribute('data-lat')
    # 得到纬度
    weidu = i.get_attribute('data-lon')
    new_lis.append(flight_name)
    new_lis.append(ph)
    new_lis.append(jindu)
    new_lis.append(weidu)
    #print(flight_name,ph,jindu,weidu)

#将 L转换成字典格式

#print(tup)
# dic = list(tup)
# n = 0
# ll = []
# #获取需要数据
# for j in dic:
#     n+=1
#     # 获取到达机场代码
#     flg_code = j['iata']
#     # 获取到达机场名称
#     # flg_name = j['name']
#     # 获取到达机场经度
#     flg_jingdu = j['lat']
#     # 获取到达机场纬度
#     flg_weidu = j['lon']
#     list1 = ['malaysia', flg_code, flg_jingdu, flg_weidu]
#     ll.append(list1)
    # print(list1)
    #print('打印次数：', n, '起飞机场代码：','malaysia' , '到达机场代码：', flg_code, '到达机场经度：', flg_jingdu, '到达机场纬度：',flg_weidu)

# 写入csv文件中
# name = ['F_code(起飞机场)', 'A_code（到达机场）', 'ar_lat（经度）', 'ar_lon（纬度）']
# test = pd.DataFrame(columns=name, data=ll)
# test.to_csv('D:\马来西亚机场连接数据.csv')
