# coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
driver=webdriver.Chrome()
driver.get("https://www.imooc.com/user/setbindsns")
driver.find_element_by_name('email').send_keys('13212575740')
driver.find_element_by_name('password').send_keys('spongebob.')
driver.find_element_by_css_selector('.moco-btn').click()
time.sleep(5)
#driver.find_element_by_link_text('个人信息').click()
# driver.find_element_by_xpath("//a[@class='on']//i[@class='icon-right2']").click()
#使用xpath过多会导致查找效率降低
driver.find_element_by_xpath("//a[contains(@href,'setprofile')]").click()
driver.find_element_by_css_selector('.pull-right').click()
# driver.find_elements_by_css_selector('.moco-form-control')[7].find_elements_by_tag_name('option')[4].click()
select_element = driver.find_elements_by_css_selector('.moco-form-control')[7]
Select(select_element).select_by_value('11')
# time.sleep(5)
# driver.find_element_by_xpath("//div[@id='main']//li[5]//a[1]").click()