#coding = utf-8
import configparser
class ReadIni:
    '''
    读取配置文件，默认路径为“D:\自动化测试学习\config\LocalElement.ini”
    '''
    def __init__(self):
        self.data = self.load_ini("D:\自动化测试学习\config\LocalElement.ini")

    def load_ini(self, path):
        cf = configparser.ConfigParser()
        cf.read(path)
        return cf

    def get_value(self, node, key):
        '''
        获得配置文件对应 node 下 key 的 value
        :param node: 配置文件中的节点
        :param key: 节点下的 key
        :return: key 对应的 value
        '''
        return self.data.get(node, key)

readini = ReadIni()





