import pymysql as py


def getconnectmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')
db = getconnectmysql()
cur = db.cursor()


def select_china():
    sql = "DELETE from ydyl_copy WHERE (Take_code,Landing_code) in " \
          "(SELECT Take_code,Landing_code from " \
          "(SELECT Take_code,Landing_code FROM ydyl_copy GROUP BY " \
          "Take_code,Landing_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
          "(SELECT id from (SELECT id FROM ydyl_copy GROUP BY Take_code,Landing_code " \
          "HAVING COUNT(*)>1) s2);"
    cur.execute(sql)
    db.commit()
    print("开始执行select_china方法")


if __name__ == '__main__':
    select_china()

    # 关闭数据库
    db.close()
