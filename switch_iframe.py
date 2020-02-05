#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
driver=webdriver.Chrome()
driver.get("https://www.imooc.com/user/setbindsns")
driver.find_element_by_name('email').send_keys('13212575740')
driver.find_element_by_name('password').send_keys('spongebob.')
driver.find_element_by_css_selector('.moco-btn').click()
time.sleep(5)
driver.get('https://www.imooc.com/wenda/save')
driver.find_element_by_id('ques-title').send_keys('title')
driver.switch_to.frame('ueditor_0')
print('已经切换到iframe')
time.sleep(3)
element = driver.find_element_by_tag_name('p')
print('是否获得了这个元素？', element)
ActionChains(driver).move_to_element(element).click().send_keys('test text').perform()
