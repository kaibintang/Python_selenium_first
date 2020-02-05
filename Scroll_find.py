#coding=utf-8
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get("https://www.imooc.com/read")
js = 'document.documentElement.scrollTop=100000;'
flag = True
while flag:
    elements = driver.find_elements_by_css_selector('.title')
    for element in elements:
        print(element.text)
        if element.text == '从 0 开始学爬虫':
            element.click()
            flag = False
    driver.execute_script(js)
    time.sleep(3)



