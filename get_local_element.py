#coding=utf-8
import sys
sys.path.append('D:\\自动化测试学习')
from read_init import ReadIni
from open_browser import selenium_driver
readini = ReadIni()
data = readini.get_value('element','username')
data_info = data.split('>')
by = data_info[0]
value = data_info[1]
print(by,'----->',value)
selenium_driver.get_url("https://www.imooc.com/user/newlogin")

selenium_driver.send_value(by,value,'test')


