# 导入相关联的包
import requests
import time
import random
import socket
import http.client
import pymysql
from bs4 import BeautifulSoup
import csv


def getContent(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }  # request 的请求头
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)  # 请求url地址，获得返回 response 信息
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:  # 以下都是异常处理
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    print('request success')
    return rep.text  # 返回的 Html 全文


def getdata(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:
        temp = []
        date = day.find('h1').string
        temp.append(date)  # 添加日期
        inf = day.find_all('p')
        weather = inf[0].string  # 天气
        temp.append(weather)
        temperature_highest = inf[1].find('span').string  # 最高温度
        temperature_low = inf[1].find('i').string  # 最低温度
        temp.append(temperature_highest)
        temp.append(temperature_low)
        final.append(temp)
    print('getDate success', final)
    return final


def writedata(data, name):
    with open(name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)
    print('write_csv success')


def createtable():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "hh226752", "flightradar24")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 显示数据库版本（可忽略，作为个栗子）

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS WEATHER")
    # 使用预处理语句创建表
    sql = """CREATE TABLE WEATHER (
             w_id int(8) not null primary key auto_increment, 
             w_date  varchar(20) NOT NULL ,
             w_detail  varchar(30),
             w_temperature_low varchar(10),
             w_temperature_high varchar(10)) DEFAULT CHARSET=utf8"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()
    print('create table success')


def insertdata(datas):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "hh226752", "flightradar24")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        # 批量插入数据
        cursor.executemany('insert into WEATHER(w_id, w_date, w_detail, w_temperature_low, w_temperature_high)'
                           ' value(null, %s,%s,%s,%s)', datas)

        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print('插入时发生异常' + e)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
    print('insert data success')

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101210101.shtml'
    html = getContent(url)    # 获取网页信息
    result = getdata(html)  # 解析网页信息，拿到需要的数据
    # writedata(result, 'D:/weather.csv')  # 数据写入到 csv文档中
    # createtable() #表创建一次就好了，注意
    # insertData(result)  # 批量写入数据
    print('my frist python file')

#
