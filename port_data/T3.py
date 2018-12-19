import demjson
import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = db.cursor()

dict1 = open(r"C:\Users\dell\Desktop\python\chuanzhi.txt")
data = dict1.read()
data.replace(" ", '')
zidian = data.replace("\n","")

aa=zidian.replace("},",'}||')
a=aa.split("||")
for x in a:
    b = demjson.decode(x)
    #print(b)
    #port = b["PORT_ID"]   # 港口ID
    IMO = b["IMO"]
    MMSI = b["MMSI"]
    CALLSIGN = b["CALLSIGN"]
    SHIPNAME = b["SHIPNAME"]   # 船名
    NEXT_PORT_NAME = b["NEXT_PORT_NAME"]   #下个港口名字
    NEXT_PORT_COUNTRY = b["NEXT_PORT_COUNTRY"]  #下个港口国家
    lat = b["LAT"]   # 纬度
    lon = b["LON"]   # 经度
    country = b["COUNTRY"]   # 国家
    country_code = b["CODE2"] # 国家代码
    print(SHIPNAME,NEXT_PORT_NAME,NEXT_PORT_COUNTRY,lat,lon,country,country_code)
    # sql = "insert into ydyl_vessels(country,country_code,port_name,lat,lon)" \
    #       " values(%s,%s,%s,%s,%s)"
    # param = (country,country_code, port_name, lat, lon)
    # cursor.execute(sql, param)
    # db.commit()

dict1.close()
db.close()
