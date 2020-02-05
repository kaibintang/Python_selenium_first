#coding = utf-8
from selenium import webdriver
options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'F:\\Download\\','profile.default_content_setting.popups':0}
options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome(options=options)
driver.get('https://www.imooc.com/mobile/app')
driver.find_element_by_link_text('Android 下载').click()
