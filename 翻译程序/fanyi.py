import urllib.request
import urllib.parse
import json
import pymysql as py


# 从数据库中读取数据
def getconnection():
    return py.connect(host='localhost', user='root', password='hh226752',db = 'flightradar24', charset = 'utf8' )

# 加载数据库中数据
conn = getconnection()
cur = conn.cursor()
cn = cur.execute('select Airports_name from test')

# 将数据转到 list1中，数据类型为list
rows = cur.fetchall()
rows = list(rows)
list1 = []
for i in rows:
    list1.append(list(i))

list2 = []
for i in list1:
    list2.append(i[0])
# 将数据翻译
print(list2)
list3 = ['Bost Airport', 'Chaghcharan Airport', 'Farah Airport', 'Herat International Airport']
result = []


def fanyi():
    for i in list3:
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {}
        data['i'] = i
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = '1527480457870'
        data['sign'] = 'abf2d2301303ac6d8ae48c532c631060'
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_REALTIME'
        data['typoResult'] = 'false'
        data = urllib.parse.urlencode(data).encode('utf-8')
        response = urllib.request.urlopen(url, data)
        html = response.read().decode('utf-8')
        target = json.loads(html)
        result.append(target['translateResult'][0][0]['tgt'])
    print(result)

if __name__ == '__main__':
    fanyi()
# name = ['机场名称']
# test = pd.DataFrame(columns=name,data='result')
# test.to_csv(r"d:\机场名称.csv")
