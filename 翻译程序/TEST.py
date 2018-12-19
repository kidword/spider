from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

driver = webdriver.PhantomJS()

name = '菜户营 嘉莲苑'

driver.get('http://api.map.baidu.com/lbsapi/getpoint/index.html')

driver.find_element_by_id('localvalue').send_keys(name)
driver.find_element_by_class_name('button').click()
# 点击完成必须休眠
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
reslt = soup.select('#no_0 p')
print(type(reslt))
l = re.findall('坐标：(.*?)</p>', str(reslt))[0]
data = l.split(',')
print(data[0], data[1])


