import pymysql as py
import datetime
from threading import Thread

Today = datetime.datetime.now()  # 获取当天时间
Today1 = Today.strftime('%Y-%m-%d')
yesterday = Today + datetime.timedelta(days=-7)
yesterday1 = yesterday.strftime('%Y-%m-%d')


def connection():
    db = py.connect(host='localhost', port=3306, user="root", password='hh226752', db='flightradar24', charset="utf8")
    return db


def select():
    conn = connection()
    cur = conn.cursor()
    sql1 = 'select address,apartment,area from lj_xb where dtime="{}"'.format(Today1)
    cn = cur.execute(sql1)
    rows = cur.fetchall()
    rows = list(rows)
    return rows


def dorp_data():
    conn = connection()
    cur = conn.cursor()
    drop_sql = "DELETE from lj_xb WHERE (address, apartment,area,dtime) in " \
               "(SELECT address, apartment,area,dtime from " \
               "(SELECT address, apartment,area,dtime FROM lj_xb " \
               "GROUP BY address, apartment,area,dtime HAVING COUNT(*)>1) s1) AND  id NOT in " \
               "(SELECT id from (SELECT id FROM lj_xb " \
               "GROUP BY address, apartment,area,dtime HAVING COUNT(*)>1) s2)"
    cur.execute(drop_sql)
    conn.commit()
    conn.close()
    print("删除完成...")


def updata():
    rows = select()
    conn1 = connection()
    n = 1
    for i in range(len(rows)):
        address = rows[i][0]
        apartment = rows[i][1]
        area = rows[i][2]
        cur = conn1.cursor()
        sql = "update lj_xb set c_price=(select (b.z_price-a.z_price) as plaquenum from" \
              "(select * from lj_xb where address='{0}' and dtime='{1}' and apartment='{2}' and area='{3}') a," \
              "(select * from lj_xb where address='{4}' and dtime='{5}' and apartment='{6}' and area='{7}') b) where " \
              "address='{8}' and dtime='{9}' and apartment='{10}' and area='{11}'".format \
            (address, yesterday1, apartment, area, address, Today1, apartment, area, address, Today1, apartment, area)
        cur.execute(sql)
        conn1.commit()
        print('执行第{}次sql'.format(n))
        n += 1
    conn1.close()


def run():
    for i in range(5):
        t_content = Thread(target=updata)
        t_content.start()
        t_content.join()


if __name__ == '__main__':

    # dorp_data()
    # updata()
    run()
