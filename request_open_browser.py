import requests
import json


class request_webdriver:
    def __init__(self):
        self.driver = self.chrome_driver()

    def chrome_driver(self):
        """
        使用chrome浏览器创建一个webdriver对象
        :return: 带sessionId的url
        """
        url = 'http://127.0.0.1:4444/wd/hub/session/'
        data = json.dumps({
            'desiredCapabilities': {
                'browserName': 'chrome'
            }
        })
        res = requests.post(url, data).json()
        session = res['sessionId']
        driver = url + session
        return driver

    def get_url(self, url):
        """
        打开网站
        :param url: 网站链接
        :return:
        """
        base_url = self.driver + '/url'
        data = json.dumps({
            "url": url
        })
        requests.post(base_url, data).json()

    def find_element_by_name(self, id_name):
        """
        通过name查找元素
        :return: element的值
        """
        base_url = self.driver + '/element'
        data = json.dumps({
            "using": 'name',
            "value": id_name
        })
        res = requests.post(base_url, data).json()['value']['element-6066-11e4-a52e-4f735466cecf']
        print(res)
        return res

'''
使用main方法
'''
if __name__ == "__main__":
    request_driver = request_webdriver()
    request_driver.get_url('https://www.imooc.com/u/index/allcourses')
    request_driver.find_element_by_name('password')
