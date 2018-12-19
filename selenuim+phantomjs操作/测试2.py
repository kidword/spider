from selenium import webdriver
browser=webdriver.PhantomJS()

browser.get("https://www.zhipin.com/job_detail/?query=python&scity=101010100&industry=&position=")

tit = browser.find_elements_by_css_selector('#main > div > div.job-list > ul > li> div > div.info-primary > h3 > a > div.job-title')
name = browser.find_elements_by_css_selector('#main > div > div.job-list > ul > li> div > div.info-company > div > h3 > a')
dizhi = browser.find_elements_by_css_selector('#main > div > div.job-list > ul > li> div > div.info-primary > p ')
time = browser.find_elements_by_css_selector('#main > div > div.job-list > ul > li> div > div.info-publis > p')

tit_lis = []
for i in tit:
    tit_lis.append(i.text)
name_lis = []
for i in name:
    name_lis.append(i.text)
dizhi_lis = []
for i in dizhi:
    dizhi_lis.append(i.text)
time_lis = []
for i in time:
    time_lis.append(i.text)

new_info = zip(tit_lis,name_lis,dizhi_lis,time_lis)

for i in new_info:
    print(list(i))

# browser.close()