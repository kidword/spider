import pymysql as py
import requests
from selenium import webdriver
from selenium.webdriver.common import keys
import time
from bs4 import BeautifulSoup
import lxml
import re

driver = webdriver.PhantomJS()
def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

conn = getmysql()
cur = conn.cursor()
cn = cur.execute('select qu,name from zufang')
rows = cur.fetchall()
rows = list(rows)

driver.get('http://api.map.baidu.com/lbsapi/getpoint/index.html')
names = '富莱茵花园'
driver.find_element_by_id('localvalue').send_keys(names)
driver.find_element_by_class_name('button').click()
time.sleep(1)
try:
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    reslt = soup.select('#no_0 p')
    print(reslt)
    for area in reslt:
        areas = area.select('br')[0].next_sibling
        print(areas)
except:
    print('未找到元素')

#driver.save_screenshot('ditu.png')
driver.quit()