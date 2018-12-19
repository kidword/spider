from selenium import webdriver
browser=webdriver.PhantomJS()

browser.get("https://www.weibo.com")

#browser.save_screenshot("new.jpg")
browser.close()
