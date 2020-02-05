# coding:utf-8
import json

class Handle_json():

    def __init__(self):
        self.data = self.read_data()

    def read_data(self):
        with open('./config/cookie.json') as fp:
            data = json.load(fp)
            return data

    def get_data(self):
        return self.data

    def write_data(self, cookie):
        with open('./config/cookie.json','w') as fp:
            fp.write(json.dumps(cookie))


handle_json = Handle_json()