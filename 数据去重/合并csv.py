import pandas as pd
import pymysql

def getdata():
    conn = pymysql.connect(host = 'localhost',user = 'root',password = 'hh226752',db = 'flightradar24',charset = 'utf8')
    return conn
con = getdata()

cur = con.cursor()
cn = cur.execute('select * from flight')
rows = cur.fetchall()

cur1 = con.cursor()
cn1 = cur1.execute('select * from flight_xin')
rows1 = cur1.fetchall()

list1 = []
for i in rows:
    list1.append(list(i))
list2 =[]
for i in rows1:
    list2.append(list(i))
print(list1[0])
print(list2[0])
list3 = list1+list2

# 先将list3写入csv文件中
name = ['ID','Take_off_airport_country','Take_off_airport_name','Take_off_airport_code','Take_off_airport_alt','Take_off_airport_lon','Landing_airport_country','Landing_airport_name','Landing_airport_code','Landing_airport_city','Landing_lat','Landing_lon']
test = pd.DataFrame(columns=name,data=list3)
test.to_csv(r'd:\flight_xin.csv')
# 删除重复机场代码




con.close()