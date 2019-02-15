import pymysql as py
import datetime

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
    sql1 = 'select address,apartment,area from lj_test_copy where dtime="{}"'.format(Today1)
    print(sql1)
    cn = cur.execute(sql1)
    rows = cur.fetchall()
    rows = list(rows)
    return rows


def updata():
    rows = select()
    conn1 = connection()
    n = 1
    for i in range(len(rows)):
        address = rows[i][0]
        apartment = rows[i][1]
        area = rows[i][2]
        cur = conn1.cursor()
        sql = "update lj_test_copy set c_price=(select (b.z_price-a.z_price) as plaquenum from" \
              "(select * from lj_test_copy where address='{0}' and dtime='{1}' and apartment='{2}' and area='{3}') a," \
              "(select * from lj_test_copy where address='{4}' and dtime='{5}' and apartment='{6}' and area='{7}') b) where " \
              "address='{8}' and dtime='{9}' and apartment='{10}' and area='{11}'".format \
            (address, yesterday1, apartment, area, address, Today1, apartment, area, address, Today1, apartment, area)
        cur.execute(sql)
        conn1.commit()
        print('执行第{}次sql'.format(n))
        n += 1
    conn1.close()

if __name__ == '__main__':
    updata()
