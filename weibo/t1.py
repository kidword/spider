#coding:utf-8
'''使用selenium 获取cookie '''
from selenium import webdriver
from selenium.webdriver.common import keys
import time
import requests
from bs4 import BeautifulSoup
import lxml

# 使用phantomjs驱动
driver = webdriver.PhantomJS()

# 启动登入页面url
driver.get('https://login.sina.com.cn/signup/signin.php?entry=sso')

# 得到cookie值
def getcookie(username,password):
    # 模拟输入账号密码
    try:
        driver.find_element_by_name('username').send_keys(username)
    except:
        print('没找到username元素')
    try:
        driver.find_element_by_name('password').send_keys(password)
    except:
        print('没找到password元素')

    # 模拟点击登入按钮
    try:
        driver.find_element_by_xpath('//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input').click()
    except:
        print('没找到登入按钮')

    # 必须在登成功以后设置等待时间，否则获取不到登入后的cookie
    time.sleep(10)

    # 得到cookie
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    return cookiestr
getcookie('账号','密码')

# 得到个人首页信息
def Myweibo():
    url = 'https://weibo.com/u/5591104737/home?wvr=5'
    headers = {'cookie':getcookie(),
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    req = requests.get(url=url,headers=headers).text
    return req

# 快照
driver.save_screenshot('weibo.png')

#退出
driver.quit()