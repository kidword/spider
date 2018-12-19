#获取全球所有机场信息
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import requests
import re
import pandas as pd

browser=webdriver.Chrome()
browser.get("https://www.flightradar24.com/data/airports")
lis=browser.find_elements_by_css_selector("#tbl-datatable > tbody > tr> td> a")

#列表去除'' ,并且添加到lis_new中
lis_new = []
for i in lis:
    if len(i.text)>=1:
        L = i.text.replace("'", "")
        L1 = L.replace("(", "")
        L2 = L1.replace(")", "")
        L3 = L2.replace(",", "")
        L4 = L3.replace(" ", "-")
        lis_new.append(L4)

# 去除lis_new列表中， （）  '   然后用 - 连接所有单词
#print(lis_new)

#获得所有国家url放入 U_lis列表中
U_lis = []
for i in lis_new:
    url = 'https://www.flightradar24.com/data/airports/{}'
    url_lis = url.format(i)
    U_lis.append(url_lis)
#print('所有国家url列表：',U_lis)


#解析U_lis 找出所有国家机场
new_lis = []
for i in U_lis:
    browser.get(i)
    lis = browser.find_elements_by_css_selector("#tbl-datatable > tbody > tr > td > a")
    for j in lis:
        # 获取机场名称
        flight_name = j.get_attribute('title')
        # 获取中国机场名称
        city = j.text
        # 获取机场号码
        ph = j.get_attribute('data-iata')
        # 得到经度
        jindu = j.get_attribute('data-lat')
        # 得到纬度
        weidu = j.get_attribute('data-lon')
        list1 = [flight_name, ph, jindu, weidu]
        new_lis.append(list1)
        print(j.text)
        print('机场名称：',flight_name,'机场号码:',ph,'机场经度：', jindu,'机场纬度：',weidu)

name = ['F_code(机场名称)','A_code(机场代码)','ar_lat(经度)','ar_lon（纬度）']
test = pd.DataFrame(columns=name,data=new_lis)
test.to_csv('D:\世界机场数据.csv')

