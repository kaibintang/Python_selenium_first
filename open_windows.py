#coding=utf-8
from selenium import webdriver
import selenium.webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
time.sleep(3)
driver.get("https://www.imooc.com/user/setbindsns")
driver.find_element_by_name('email').send_keys('13212575740')
driver.find_element_by_name('password').send_keys('spongebob.')
driver.find_element_by_class_name('moco-btn').click()
# 进入个人设置页面
time.sleep(1)
#打开微博绑定页面
driver.find_elements_by_class_name('inner-i-box')[1].find_element_by_class_name('moco-btn-normal').click()
time.sleep(20)
current_handle = driver.current_window_handle
handle_list = driver.window_handles
print(handle_list)
for i in handle_list:
    if i != current_handle:
        driver.switch_to.window(i)
        title = EC.title_contains('网站连接')
        if title(driver):
            break

time.sleep(2)
driver.find_element_by_id('userId').send_keys('aaaa')
time.sleep(5)
driver.close()
