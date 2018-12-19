import psycopg2
import time
import os
import datetime

while True:
    conn = psycopg2.connect(host='47.95.10.198', user='postgres', password='qwe123', database='zxdsj')
    cur = conn.cursor()

    # 获取时间
    t = datetime.datetime.now().strftime('%Y-%m-%d')
    timeArray = time.strptime(t, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    data = timeStamp-172800
    timearray = time.localtime(data)
    dtime = time.strftime("%Y-%m-%d", timearray)
    print(dtime)

    # 删除文件中图片
    try:
        sql3 = "select * from qg_server where dttime<'{}'".format(dtime)
        cur.execute(sql3)
        rows = cur.fetchall()
        print(rows)
        for i in rows:
            data = list(i)
            try:
                os.remove(data[1])
            except:
                print("pass1")
    except:
        print("删除错误")

    # 删除数据库中小于3天前的数据
    try:
        sql2 = "DELETE from qg_server where dttime<'{}'".format(dtime)
        cur.execute(sql2)
        conn.commit()
    except:
        pass
    conn.close()
    time.sleep(86400)
