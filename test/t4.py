from selenium import webdriver
import pymysql as py
browser = webdriver.PhantomJS()


conn = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')


url = 'https://www.fmprc.gov.cn/web/zwjg_674741/zwzlg_674757/bmdyz_674769/'
browser.get(url)
name = browser.find_elements_by_css_selector("body > div.cbody > div.rebox.wjbox > div.rebox_r.fr > div.rebox_news.jgbox_news > table > tbody > tr> td > table > tbody > tr > td> a")

n=0
for i in name:
    n+=1
    data = i.text
    print(data,n)
    # con = conn.cursor()
    # sql = "insert into dashiguan_copy(name) values(%s)"
    # params = (data)
    # con.execute(sql, params)
    # conn.commit()
conn.close()

