#coding= utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get('http://www.imooc.com')
LOCATOR = (By.ID, 'name')
EC.visibility_of_element_located(LOCATOR)
EC.visibility_of_all_elements_located
element = driver.find_element_by_name('password')
driver.find_element()
element.send_keys('aaaa')