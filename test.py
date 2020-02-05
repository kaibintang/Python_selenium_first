# coding=utf-8
from selenium import webdriver
import time
import json
import handle_json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from pykeyboard import PyKeyboard

driver = webdriver.Chrome()
driver.get("https://www.imooc.com/u/index/allcourses")
driver.delete_all_cookies()
'''
cookies = handle_json.handle_json.get_data()
# 将json类型转化为 Python字典类型
cookie_dict =json.dumps(cookies)
for cookie in cookie_dict:
    for value in cookie.values():
        if (value == 'False') | (value == 'True'):
            value = value.lower()
print(cookies)
'''
cookie = {
"domain": "imooc.com",
"expiry": 1581407319,
"httpOnly": False,
"name": "apsid",
"path": "/",
"secure": False,
"value": "A0NWQ3MjEwN2VkYzAwMzc2NTJkN2YyMTAwZDIzNDIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANzczMjg1MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrYWliaW50YW5nQG91dGxvb2suY29tAAAAAAAAAAAAAGE4NGM4OWJlMDg1NjVjM2I5MTk0ZjFmMjZiNzIzYjcA2CE5XtghOV4%3DYz"
}
driver.add_cookie(cookie)
time.sleep(2)
driver.get("https://www.imooc.com/u/index/allcourses")

'''
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

driver.get("chrome://settings/importData")
# time.sleep(10)
pykey = PyKeyboard()
pykey.tap_key(pykey.enter_key)
pykey.tap_key(pykey.shift_key)
pykey.type_string('C:\\Users\\mayn\\Desktop\\bookmarks_2020_2_1.html')
time.sleep(2)
pykey.tap_key(pykey.enter_key)
'''