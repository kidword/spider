import pymysql

conn = pymysql.connect(host='localhost', user='root',password='hh226752', db='flightradar24', charset='utf8')


def run_world_copy():
    print("执行删除world_copy表重复数据")
    sql = "DELETE from world_copy WHERE (Airports_code) in " \
          "(SELECT Airports_code from " \
          "(SELECT Airports_code FROM world_copy GROUP BY " \
          "Airports_code HAVING COUNT(*)>1) s1) AND  id NOT in " \
          "(SELECT id from (SELECT id FROM world_copy GROUP BY Airports_code " \
          "HAVING COUNT(*)>1) s2);"
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()
    print('执行完成')
if __name__ == '__main__':
    run_world_copy()