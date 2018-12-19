import demjson
import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = db.cursor()

dict1 = open(r"C:\Users\dell\Desktop\python\port1.txt")
data = dict1.read()
data.replace(" ", '')
zidian = data.replace("\n","")
aa=zidian.replace("},",'}||')
a=aa.split("||")
n = 0
for x in a:
    b = demjson.decode(x)
    port = b["PORT_ID"]
    port_name = b["PORT_NAME"]
    lat = b["CENTERX"]
    lon = b["CENTERY"]
    country = b["COUNTRY"]
    country_code = b["COUNTRY_CODE"]
    print(port)
    # print(port_name,lat,lon,country,country_code)
    # sql = "insert into ydyl_port(country,country_code,port_name,lat,lon)" \
    #       " values(%s,%s,%s,%s,%s)"
    # param = (country,country_code, port_name, lat, lon)
    # cursor.execute(sql, param)
    # db.commit()

dict1.close()
db.close()
