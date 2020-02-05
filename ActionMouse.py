#coding=utf-8
from selenium import webdriver
import time
# 导入鼠标事件
from selenium.webdriver.common.action_chains import ActionChains
# 导入键盘事件
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.imooc.com/")
# element = driver.find_elements_by_css_selector('.item')[2]
# ActionChains(driver).move_to_element(element).perform()
#driver.find_element_by_link_text('Python').click()
driver.find_element_by_id('js-signin-btn').click()
time.sleep(2)
# Ctrl+F5 强制刷新
ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL).perform()
