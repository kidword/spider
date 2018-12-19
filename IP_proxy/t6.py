import requests
from user_agents import agents
import random
import threading
import re
import json


# 执行1  得到html
def get_html(urls):
    por = ["113.13.29.63:8118", "222.181.10.243:8118"]
    response = requests.get(
        url=urls,
        headers={"User-Agent": random.choice(agents)})
    # print(response.text)
    html = response.text
    get_proxy(html)


# 执行2 解析html
def get_proxy(html):
    L = re.search('arrRoutes=\[(.*?)\]', html, re.S).group(1)
    ss = re.findall('{.*?}', L)
    lis = []
    try:
        for j in ss:
            l = json.loads(j)
            flg_code = l['iata']  # 机场代码
            flg_name = l['name']  # 机场名称
            flg_city = l['city']  # 机场所在城市
            flg_country = l['country']  # 机场所在国家
            flg_lat = l['lat']  # 机场的经度
            flg_lon = l['lon']  # 机场的纬度
            data = flg_code+flg_name+flg_city+flg_country+flg_lat+flg_lon
            lis.append(data)
            print(flg_code,flg_name,flg_city,flg_country,flg_lat,flg_lon)
    except AttributeError:
        print('没有航线信息的机场：')
    except requests.exceptions.ReadTimeout:
        print('请求timeout超时')
    except requests.exceptions.ConnectionError:
        print("请求错误")
    test_proxies(lis)
    # 从html中解析出来的数据添加到lis中


# 执行3 测试数据是否正常
def test_proxies(lis):
    lis = lis  # 接收数据
    # 下面对lis数据进行遍历，开启多线程
    for proxy in lis:
        test = threading.Thread(target=thread_test_proxy, args=(lis,))
        test.start()


# 执行4 对数据进行测试
def thread_test_proxy(lis):
    thread_write_proxy(lis)


# 执行5 对数据进行写入：
def thread_write_proxy(lis):
    with open(r"./test.txt","w+") as f:
        print("正在写入",lis)
        f.write(lis + '\n')
        print("录入完成！！！")


if __name__ == '__main__':
    # 得到所有url
    # 获取起飞机场的所有信息
    for i in ["fnc"]:
        url = "http://www.flightradar24.com/data/airports/{}/routes"
        urls = url.format(i)
        get_html(urls)

