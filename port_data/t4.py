import demjson
import pymysql

dict1 = open(r"C:\Users\dell\Desktop\python\china_port.txt")
data = dict1.read()
data.replace(" ", '')
zidian = data.replace("\n","").replace("\t","")
aa = zidian.replace("},",'}||')
a = aa.split("||")

db = pymysql.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = db.cursor()

for x in a:
    b = demjson.decode(x)
    Ename = b["pinyin"].upper()   # 英文名转大写
    Zname = b["name"]             # 中文名
    country = "China"             # 港口国家
    country_code = "CN"           # 港口国家简称
    lat = b["slat"]               # 纬度
    lon = b["slon"]               # 经度
    print(b)
    # print(port_name,lat,lon,country,country_code)
    sql = "insert into ydyl_port(country,country_code,port_name,lat,lon)" \
          " values(%s,%s,%s,%s,%s)"
    param = (country,country_code, Zname, lat, lon)
    cursor.execute(sql, param)
    db.commit()

dict1.close()

# str2 = '{id:4,name:"丹东", py: "dd", pinyin: "dandong",slat:39.83133,slon:124.1613,latlon:"' \
# '{lon:[124,124.22,124.22,124],lat:[39.9,39.9,39.6,39.6]}"}'
# print(demjson.decode(str2))