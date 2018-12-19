# 读取数据库qu和name字段去网页上搜索坐标信息放到数据库中
import pymysql as py
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import threading

driver = webdriver.PhantomJS()


# 读取数据库数据
def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

conn = getmysql()
cur = conn.cursor()
cn = cur.execute('select * from ydyl_university')
rows = cur.fetchall()

rows = list(rows)


# 得到名字列表
def getname():
    name_lis = []
    for lis in rows:
        name_lis.append(list(lis))
    return name_lis
l = getname()

# 得到地理位置信息


def getarea():
    global soup
    driver.get('http://api.map.baidu.com/lbsapi/getpoint/index.html')
    for name in l:
        names = name[1]
        #print(name[1])
        driver.find_element_by_id('localvalue').send_keys(names)
        driver.find_element_by_class_name('button').click()
        # 点击完成必须休眠
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        reslt = soup.select('#no_0 p')
        for area in reslt:
            areas = area.select('br')[0].next_sibling
            print(areas)
            ar = areas[3:].split(',')
            try:
                cur = conn.cursor()
                sql = "insert into num(qu,name,price,d_price,huxing,mianji,louceng,chaoxiang,lat,lon) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = (name[1],name[2],name[3],name[4],name[5],name[6],name[7],name[8],ar[0],ar[1])
                cur.execute(sql, params)
                conn.commit()
            except:
                areas = area.select('br')[1].next_sibling
                ar = areas[3:].split(',')
                con = conn.cursor()
                sql = "insert into num(qu,name,price,d_price,huxing,mianji,louceng,chaoxiang,lat,lon) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = (name[1],name[2],name[3],name[4],name[5],name[6],name[7],name[8],ar[0],ar[1])
                con.execute(sql, params)
                conn.commit()
        driver.find_element_by_id('localvalue').clear()

if __name__ == '__main__':
    Thread1 = threading.Thread(target=getarea)
    threads = [Thread1]
    for i in threads:
        i.start()
        i.join()
    driver.quit()


