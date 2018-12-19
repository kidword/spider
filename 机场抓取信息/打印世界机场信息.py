'''
得到222个国家机场的 国家名称、机场代码、机场经度、机场纬度
'''
from selenium import webdriver
import pymysql

connent = pymysql.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = connent.cursor()
browser = webdriver.PhantomJS()
browser.get("https://www.flightradar24.com/data/airports")
title = browser.find_elements_by_css_selector('#tbl-datatable > tbody > tr> td> a')

# C_lis得到所有国家名称列表
C_lis = []
for i in title:
    if len(i.text) > 1:
        L = i.text.replace("'", "")
        L1 = L.replace("(", "")
        L2 = L1.replace(")", "")
        L3 = L2.replace(",", "")
        L4 = L3.replace(" ", "-")
        C_lis.append(L4)
print('国家数量：', len(C_lis))
# print(C_lis)

# #得到所有国家的url
url_list = []
for i in C_lis:
    url = "https://www.flightradar24.com/data/airports/"
    url_list.append(url+i)

for i in C_lis:
    url = 'https://www.flightradar24.com/data/airports/{}'
    # 开启新页面，进行解析网页  获取 （机场代码） （机场经度） （机场纬度）
    browser.get(url.format(i))
    print(i)
    title_xin = browser.find_elements_by_css_selector('#tbl-datatable > tbody > tr> td> a')
    for j in title_xin:
        if len(j.text) > 1:
            flight_name = j.get_attribute('title')
            # 获取机场号码
            ph = j.get_attribute('data-iata')
            # 得到经度
            jindu = j.get_attribute('data-lat')
            # 得到纬度
            weidu = j.get_attribute('data-lon')
            print(i, flight_name, ph, jindu, weidu)
            sql = "insert into test(Countries,Airports_name,Airports_code,Airports_ar_lat,Airports_ar_lon)" \
                  " values(%s,%s,%s,%s,%s)"
            param = (i, flight_name, ph, jindu, weidu)
            cursor.execute(sql, param)
            connent.commit()

connent.close()
browser.close()

