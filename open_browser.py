# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import sys
sys.path.append('E:\\Python_selenium_first')
from read_init import readini
from pykeyboard import PyKeyboard
from selenium.webdriver.common.keys import Keys
import time
from handle_json import handle_json

# 类使用
class SeleniumDriver:
    def __init__(self, browser):
        self.driver = self.open_browser(browser)

    def open_browser(self, browser):
        try:
            if browser == 'chrome':
                options = webdriver.ChromeOptions()
                prefs = {'download.default_directory': 'F:\\Download\\', 'profile.default_content_setting.popups': 0}
                options.add_experimental_option('prefs', prefs)
                driver = webdriver.Chrome(options=options)
            elif browser == 'firefox':
                profile = webdriver.FirefoxProfile()
                profile.set_preference('browser.download.dir','F:\\Download\\')
                profile.set_preference('browser.download.folderList',2)
                profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/zip')
                driver = webdriver.Firefox(firefox_profile=profile)
            else:
                driver = webdriver.Edge()
            return driver
        except:
            print('打开浏览器失败')
            return None

    def get_url(self, url):
        """
        打开网站
        :param url: 网站链接
        :return: 正确打开网站或者报错
        """
        if self.driver is not None:
            if 'http://' in url:
                self.driver.get(url)
            elif 'https://' in url :
                self.driver.get(url)
            elif 'chrome://' in url :
                self.driver.get(url)
            else:
                print('你的url有问题')
        else:
            print('case失败')

    def handle_windows(self, *args):
        """
        根据传递的参数来控制窗口的大小
        :param args: 数量为1时做对应操作，数量为2个数字时设置窗口大小
        :return: 成功控制窗口或是返回错误信息
        """
        if len(args) == 1:
            if args[0] == 'max':
                self.driver.maximize_window()
            elif args[0] == 'min':
                self.driver.minimize_window()
            elif args[0] == 'back':
                self.driver.back()
            elif args[0] == 'go':
                self.driver.forward()
            else:
                self.driver.refresh
        elif len(args) == 2:
            self.driver.set_window_size(200, 300)
        else:
            print("你传递的参数有问题")
        time.sleep(5)
        self.driver.quit()

    def assert_title(self, title_name=None):
        """
        判断当前页面的标题是否包含参数title_name
        :param title_name: 要判断的标题名称
        :return: true or false
        """
        if title_name is not None:
            get_title = EC.title_contains(title_name)
            return get_title(self.driver)

    def open_url_is_true(self, url, title_name):
        """
        通过title判断页面是否打开正确
        """
        self.get_url(url)
        return self.assert_title(title_name)

    def close_driver(self):
        self.driver.close()

    def switch_windows(self, titlt_name=None):
        """
        切换窗口并根据参数title_name找到对应的窗口
        :param titlt_name: 正确窗口的标题
        :return: 做相应的操作
        """
        handle_list = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for i in handle_list:
            if i != current_handle:
                self.driver.switch_to.window(i)
                if self.assert_title(titlt_name):
                    break
        # self.driver.find_element_by_id('userId').send_keys('aaaa')
        # time.sleep(2)

    def element_is_display(self, element):
        '''
        判断元素是否可见
        :param element:传入的元素
        :return: 可见返回该 element，不可见返回 False
        '''
        flag = element.is_displayed()
        if flag:
            return element
        else:
            return False

    def get_element(self, ini_node, ini_key):
        '''
        通过读取配置文件的 by 和 value ，来取得相应的单个元素
        :param ini_node: 配置文件的相应节点
        :param ini_key: 节点下 key 的值
        :return: 返回获得的该元素、 False 或 None
        '''
        element = None
        by, value = self.get_local_element(ini_node, ini_key)
        try:
            if by == 'id' :
                element = self.driver.find_element_by_id(value)
            elif by == 'name':
                element = self.driver.find_element_by_name(value)
            elif by == 'css':
                element = self.driver.find_element_by_css_selector(value)
            elif by == 'class':
                element = self.driver.find_element_by_class_name(value)
            elif by == 'xpath':
                element = self.driver.find_element_by_xpath(value)
            elif by == 'tagname':
                element = self.driver.find_element_by_tag_name(value)
            else:
                element = self.driver.find_element_by_link_text(value)
            return self.element_is_display(element)
        except:
            print("根据传入的值无法查找到单个元素，请确定是否为list元素或值是否正确")
            return element

    def get_elements(self, ini_node, ini_key):
        '''
        通过读取配置文件的 by 和 value ，来取得相应的多个元素
        :param ini_node: 配置文件的相应节点
        :param ini_key: 节点下 key 的值
        :return: 获得的元素list 或者是 None
        '''
        by, value = self.get_local_element(ini_node, ini_key)
        elements = None
        element_list = []
        try:
            if by == 'id':
                elements = self.driver.find_elements_by_id(value)
            elif by == 'name':
                elements = self.driver.find_elements_by_name(value)
            elif by == 'css':
                elements = self.driver.find_elements_by_css_selector(value)
            elif by == 'class':
                elements = self.driver.find_elements_by_class_name(value)
            elif by == 'tagname':
                elements = self.driver.find_elements_by_tag_name(value)
            else:
                elements = self.driver.find_elements_by_xpath(value)
            for element in elements:
                if self.element_is_display(element) == False:
                    continue
                else:
                    element_list.append(element)
            return element_list
        except:
            print("根据传入的值无法查找到元素list，请确定值是否正确")
            return elements

    def get_level_element(self, ini_node, ini_key, node_by, node_value):
        '''
        使用参数 ini_node, ini_key查找到父级元素，再通过传入的 node_by 和 node_value 查找下级子元素
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :param node_by:子元素的查找方式
        :param node_value:根据该值查找子元素
        :return:
        '''
        element = self.get_element(ini_node, ini_key)
        node_by, node_value = self.get_local_element()
        if element == False or element == None:
            print("没有找到该值")
            return False
        try:
            if node_by == 'id':
                node_element = element.find_element_by_id(node_value)
            elif node_by == 'name':
                node_element = element.find_element_by_name(node_value)
            elif node_by == 'css':
                node_element = element.find_element_by_css_selector(node_value)
            elif node_by == 'class':
                node_element = element.find_element_by_class_name(node_value)
            else:
                node_element = element.find_element_by_xpath(node_value)
            return self.element_is_display(node_element)
        except:
            print("无法查找到该父元素下的子元素，请确定值是否正确")
            return element

    def get_list_element(self, ini_node, ini_key, index):
        '''
        使用参数 ini_node, ini_key查找到数组元素，通过 index 定位父节点 list 中的数据
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :param index: 下标
        :return: 数组元素 list 中对应 index 的值
        '''
        elements = self.get_elements(ini_node, ini_key)
        if elements == False:
            print("该元素未显示")
        else:
            if elements != None:
                if int(index) > len(elements):
                    print('该数组的长度为',len(elements),',下标范围超限')
                    return None
                return elements[int(index)]
            else:
                print("找不到该元素")

    def send_value(self,ini_node, ini_key, key):
        '''
        使用参数 ini_node, ini_key查找到单个元素，再向元素中传值
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :param key: 向查找到的单个 element 传递的值
        :return: 正确传值或返回 None
        '''
        element = self.get_element(ini_node, ini_key)
        if element == False:
            print("该元素未显示")
        else:
            if element != None:
                element.send_keys(key)
            else:
                print("没有找到该元素，无法传值")
                return None

    def click_element(self, ini_node, ini_key):
        '''
        使用参数 ini_node, ini_key查找到单个元素，并点击该元素
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :return: 点击元素或者返回None
        '''
        element = self.get_element(ini_node, ini_key)
        if element == False:
            print("该元素未显示")
        else:
            if element!= None:
                element.click()
            else:
                print("没有找到该元素，点击失败")
                return None

    def mouse_hover(self, ini_node, ini_key):
        '''
        鼠标悬停在元素上方
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :return: False or 直接悬停
        '''
        element = self.get_element(ini_node, ini_key)
        if element == False:
            print("该元素未显示")
        else:
            ActionChains(self.driver).move_to_element(element).perform()

    def check_box_isselected(self,ini_node, ini_key, check=None):
        '''
        使用参数 ini_node, ini_key查找到单个元素，检查该元素是否被选中
        :param ini_node: 配置文件中的节点
        :param ini_key: 节点下的 key
        :param check: 该按钮是否要被选择
        '''
        element = self.get_element(ini_node, ini_key)
        if element == False:
            print("该元素未显示")
        else:
            flag = element.is_selected()
            if flag :
                if check == None:
                    self.click_element(ini_node, ini_key)
            else:
                if check != None:
                    self.click_element(ini_node, ini_key)

    def get_local_element(self,ini_node, ini_key):
        '''
        获取配置文件中对应 ini_node 下对应 ini_key 的 value
        :param ini_node: 配置文件中对应节点的值
        :param ini_key: 配置文件中节点下的 key 值
        :return: key 对应 value 的 list
        '''
        data = readini.get_value(ini_node, ini_key)
        data_info = data.split('>')
        return data_info

    def excute_js(self, js_code):
        '''
        执行对应的js语句
        :param js_code:js语句
        '''
        self.driver.execute_script(js_code)

    def js_removeAttribute(self,ini_node, ini_key, attribute):
        '''
        将该元素的相关 Attribute 删除
        :param ini_node:根据根节点查找该元素
        :param ini_key: 根据元素的 by 和 value 查找元素
        :param attribute: 要删除的 Attribute name
        :return:
        '''
        iniList = self.get_local_element(ini_node,ini_key)
        by = iniList[0]
        value = iniList[1]
        if by == 'id':
            by_key = 'getElementById'
            js = "document.%s('%s').removeAttribute('%s')" %(by_key,value,attribute)
        elif by == 'name':
            by_key = 'getElementsByName'
            js = "document.%s('%s').removeAttribute('%s')" % (by_key, value, attribute)
        elif by == 'css':
            by_key = 'getElementsByClassName'
            js = "document.%s('%s').removeAttribute('%s')" % (by_key, value, attribute)
        elif by == 'tagname':
            by_key = 'getElementsByTagName'
            js = "document.%s('%s').removeAttribute('%s')" % (by_key, value, attribute)
        else:
            print('by 字段错误，请核对')
        self.driver.execute_script(js)

    def get_selected_value(self,ini_node,ini_key, select_by, select_value, index=None):
        '''
        选中 select 标签中对应的值
        :param ini_node:  配置文件中对应节点的值
        :param ini_key: 配置文件中节点下的 key 值
        :param select_by: 枚举类型：index （通过option下标查找），text(通过option的文本查找)，value（通过option的value查找）
        :param select_value: 通过该值查找元素
        :param index: select如果是list元素，这是list的下标。
        :return:返回并选中这个对象
        '''
        selected_element = None
        #如果是层级元素，就通过index取得对应的元素。如果不是层级元素，直接获得该元素
        if index != None:
            selected_element = self.get_list_element(ini_node,ini_key,index)
        else:
            selected_element = self.get_element(ini_node,ini_key)
        #获得这个select元素之后，我们可以通过三个方法来获得该元素的值并且选中
        if select_by == 'index':
            Select(selected_element).select_by_index(select_value)
        elif select_by == 'text':
            Select(selected_element).select_by_visible_text(select_value)
        elif select_by == 'value':
            Select(selected_element).select_by_value(select_value)

    def upload_file(self, filename, ini_node = None, ini_key = None):
        '''
        上传文件方法，其中包含input类型和非input类型
        :param filename: 要上传的文件属性
        :param ini_node: 根据根节点查找该元素，为空即不查找元素
        :param ini_key: 根据元素的by和value 查找元素，为空即不查找元素
        '''
        if (ini_node == None) | (ini_key == None):
            pykey = PyKeyboard()
            # 输入法转化为英文输入法
            pykey.tap_key(pykey.shift_key)
            pykey.type_string(filename)
            pykey.tap_key(pykey.enter_key)
            return
        else:
            # 如果为False，则说明该元素不可见.需要执行js使其可见
            if self.get_element(ini_node, ini_key) == False:
                # 该 js 代码属于不良代码，需要后续解耦
                js = "document.getElementById('%s').removeAttribute('class')" % ini_key
                self.excute_js(js)
                time.sleep(3)
            # 如果为input类型，则直接能够sendKey
            if self.get_element(ini_node, ini_key).tag_name == 'input':
                self.send_value(ini_node, ini_key, filename)

    def move_to_element(self, ini_node, ini_key):
        '''
        移动鼠标到某个元素上
        :param ini_node: 根据根节点查找该元素，
        :param ini_key: 根据元素的by和value 查找元素
        :return : 返回ActionChains 语句，还需要 .perform() 才能够执行
        '''
        element = self.get_element(ini_node,ini_key)
        return ActionChains(self.driver).move_to_element(element)

    def refresh_F5(self):
        '''
        强制刷新，Ctrl+F5
        '''
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL).perform()

    def switch_iframe(self, ini_node=None, ini_key=None):
        '''
        切换到 iframe
        :param ini_node: 根据根节点查找该元素，
        :param ini_key: 根据元素的by和value 查找元素
        '''
        if (ini_node!=None) | (ini_key!= None) :
            iframe_element = self.get_element(ini_node, ini_key)
            self.driver.switch_to.frame(iframe_element)
        else:
            self.driver.switch_to_default_content()

    def switch_alert(self, option, input_str = None):
        '''
        对系统弹窗做出操作:
        1.只有弹窗，点击确定关闭
        2.有确认或取消两个按钮，选择按钮后关闭
        3.有输入框的弹窗，输入文字后点击确定按钮关闭
        :param option: 点击“确认”或“取消”
        :param input_str: 输入的字符
        '''
        alert = self.driver.switch_to.alert
        if option == 'accept':
            if input_str != None:
                alert.send_keys(input_str)
                alert.accept()
            else:
                alert.accept()
        else:
            alert.dismiss()

    def scroll_element(self, ini_node, ini_key, str):
        '''
        在指定的 elements 中“滚动”查找 text == str 的 element
        :param ini_node: 在ini文件node节点下查找元素
        :param ini_key: 根据 key 和对应的 value 查找相应元素
        :param str: 要匹配的字符串
        :return: 查找到返回True，未查找到返回False
        '''
        js = 'document.documentElement.scrollTop=100000;'
        flag = True
        while flag:
            elements = self.get_elements(ini_node, ini_key)
            for element in elements:
                if element.text == str:
                    flag = False
                    return element
            self.excute_js(js)
            time.sleep(3)
        return False

    def getcookie(self):
        '''
        得到浏览器现在的cookie
        :return: 浏览器现在的cookie
        '''
        return self.driver.get_cookies()

    def savecookie(self,cookie):
        '''
        将 cookie 保存到 json文件中
        :param cookie:
        '''
        handle_json.write_data(cookie)

    def setcookie(self):
        '''
        将 cookie.json 文件中的 cookie 添加到浏览器中去
        :return:
        '''
        self.driver.delete_all_cookies()
        cookie = handle_json.get_data()
        self.driver.add_cookie(cookie)

    def save_screenshot(self):
        '''
        保存截图到指定文件夹 E:/Python_selenium_first/Picture/ 下，提示是否保存成功
        '''
        now_time = time.strftime('%Y%m%d-%H%M%S')
        if self.driver.get_screenshot_as_file('E:/Python_selenium_first/Picture/%s.png' %now_time):
            print('%s.png 文件保存成功' %now_time)
        else:
            print('%s.png 文件保存失败' %now_time)

selenium_driver = SeleniumDriver('chrome')
selenium_driver.get_url("https://www.imooc.com/user/setbindsns")
#selenium_driver.get_url("https://www.imooc.com/")
# selenium_driver.get_url("chrome://settings/importData")
time.sleep(2)
#selenium_driver.check_box_isselected('css','.auto-cbx')
# selenium_driver.send_value('login', 'username', '13212575740')
# selenium_driver.send_value('login', 'password', 'spongebob.')
# selenium_driver.click_element('login', 'login_btn')
# time.sleep(2)
selenium_driver.save_screenshot()
'''
selenium_driver.get_url("https://www.imooc.com/read")
element = selenium_driver.scroll_element('read', 'art_title', 'mpvue原理深入解析36讲')
if element != False:
    print("已经找到该文章，点击进入")
    element.click()
else:
    print("未找到该文章")
'''
'''
selenium_driver.get_url("https://www.imooc.com/wenda/save")
selenium_driver.switch_iframe('ask', 'iframe')
time.sleep(2)
selenium_driver.move_to_element('ask', 'content').click().send_keys('this is test').perform()
'''
# selenium_driver.mouse_hover('setprofile', 'hover_img')
# selenium_driver.click_element('setprofile', 'photo')

'''
#selenium_driver.upload_file('setprofile', 'upload', 'D:\\33.png')
selenium_driver.upload_file('D:\\33.png')
#该元素是不可见的，必须要使其可见
# js = 'document.querySelectorAll("input")[3].style.display="block";'
# selenium_driver.excute_js(js)
# selenium_driver.send_value('setprofile', 'upload', 'D:\\33.png')
# selenium_driver.click_element('setprofile','upload')
# selenium_driver.send_value('setprofile', 'upload', 'C:\\Users\\BQ11\\Pictures\\表情包\\QQ图片20191217162653.jpg')

# selenium_driver.click_element('setprofile','set_click')
# selenium_driver.click_element('setprofile','edit')
# driver.find_elements_by_css_selector('.moco-form-control')[7]
#selenium_driver.get_list_element('setprofile','job','1').click()
# selenium_driver.get_selected_value('setprofile','job','value','11','1')
# Select(select_element).select_by_value('11')
#selenium_driver.click_element('css', '.showhide-search')
#selenium_driver.get_level_element('css', '.rlf-group', 'css', '.ipt-email').send_keys('aaaa')
time.sleep(2)
#selenium_driver.close_driver()
'''