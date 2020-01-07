# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import sys
sys.path.append('D:\\自动化测试学习')
from read_init import readini
import time

# 类使用
class SeleniumDriver:
    def __init__(self, browser):
        self.driver = self.open_browser(browser)

    def open_browser(self, browser):
        try:
            if browser == 'chrome':
                driver = webdriver.Chrome()
            elif browser == 'firefox':
                driver = webdriver.Firefox()
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
            elif by == 'name' :
                element = self.driver.find_element_by_name(value)
            elif by == 'css' :
                element = self.driver.find_element_by_css_selector(value)
            elif by == 'class' :
                element = self.driver.find_element_by_class_name(value)
            elif by == 'xpath':
                element = self.driver.find_element_by_xpath(value)
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
        elif select_by == 'text' :
            Select(selected_element).select_by_visible_text(select_value)
        elif select_by == 'value':
            Select(selected_element).select_by_value(select_value)



selenium_driver = SeleniumDriver('chrome')
selenium_driver.get_url("https://www.imooc.com/user/setbindsns")
#selenium_driver.get_url("https://www.imooc.com/")
time.sleep(2)
#selenium_driver.check_box_isselected('css','.auto-cbx')
selenium_driver.send_value('login', 'username', '13212575740')
selenium_driver.send_value('login', 'password', 'spongebob.')
selenium_driver.click_element('login', 'login_btn')
time.sleep(2)
selenium_driver.get_url("https://www.imooc.com/user/setbindsns")
selenium_driver.mouse_hover('setprofile', 'hover_img')
selenium_driver.click_element('setprofile', 'photo')

#该元素是不可见的，必须要使其可见
js = 'document.querySelectorAll("input")[3].style.display="block";'
selenium_driver.excute_js(js)
webdriver.Chrome().find_element_by_id('upload').send_keys('C:\\Users\\BQ11\\Pictures\\表情包\\QQ图片20191217162653.jpg')
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
#.rlf-group>.ipt-email