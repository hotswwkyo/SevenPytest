# -*- coding:utf-8 -*-
import json
import time
import requests


def is_string(value):
    return isinstance(value, (str))


class MockDataSender(object):

    API_PATH_KEY = "api_path"
    API_REQUEST_METHOD_KEY = "api_request_method"
    API_REQUEST_DATA_TYPE_KEY = "api_request_data_type"
    API_REQUEST_DATA_CONTENT_KEY = "api_request_data_content"
    API_RESPONSE = "api_response"

    def __init__(self, url):

        self.__url = url
        self.__headers = {}
        self.__api_path = None
        self.__api_request_method = None
        self.__api_request_data_type = None
        self.__api_request_data_content = None
        self.__api_response = None

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    def set_url(self, url):
        self.__url = url
        return self

    def add_header(self, key, value):
        self.__headers[key] = value

    def clear_headers(self):
        self.__headers = {}

    @property
    def api_path(self):
        """获取模拟的接口路径"""
        return self.__api_path

    @property
    def api_request_method(self):
        """获取模拟的接口的请求方法"""
        return self.__api_request_method

    @property
    def api_request_data_type(self):
        """获取模拟的接口的请求提交的数据类型,数据类型有如下类型: form表单数据(application/x-www-form-urlencoded) json(application/json) xml(text/xml) 等"""
        return self.__api_request_data_type

    @property
    def api_request_data_content(self):
        """获取模拟的接口的请求数据"""
        return self.__api_request_data_content

    @property
    def api_response(self):
        """获取模拟的接口的响应数据"""
        return self.__api_response

    def set_api_path(self, api_path):
        self.__api_path = api_path
        return self

    def set_api_request_method(self, api_request_method):
        if api_request_method.lower() in ["get", "post"]:
            pass
        else:
            raise ValueError("api_request_method must be get or post")
        self.__api_request_method = api_request_method
        return self

    def set_api_request_data_type(self, api_request_data_type):
        self.__api_request_data_type = api_request_data_type
        return self

    def set_api_request_data_content(self, api_request_data_content):
        self.__api_request_data_content = api_request_data_content
        return self

    def set_api_response(self, api_response):
        self.__api_response = api_response
        return self

    def is_set_api_res(self):
        if self.api_response is None:
            raise Warning("mock api response not set.")

    def __build_mock_data(self):

        self.is_set_api_res()
        data = {self.API_PATH_KEY: self.api_path if is_string(self.api_path) else "", self.API_RESPONSE: self.api_response}
        if is_string(self.api_request_method) and self.api_request_method:
            data[self.API_REQUEST_METHOD_KEY] = self.api_request_method

        if is_string(self.api_request_data_content) and self.api_request_data_content:
            data[self.API_REQUEST_DATA_CONTENT_KEY] = self.api_request_data_content

        if is_string(self.api_request_data_type) and self.api_request_data_type:
            data[self.API_REQUEST_DATA_TYPE_KEY] = self.api_request_data_type
        return data

    def send_mock_data(self):
        data = self.__build_mock_data()
        if self.headers:
            res_object = requests.post(self.url, data=data, headers=self.headers)
        else:
            res_object = requests.post(self.url, data=data)
        return res_object

    def clear_mock_data(self):
        res_object = requests.delete(self.url)
        return res_object


def mock():
    # 接口路径
    path = 'test/go'
    # 接口响应返回内容
    api_response = '{"orders":[{"id":1,"number":"12"},    {"id":2,"number":"27"}]}'
    # 请求方式
    api_request_method = 'get'
    # 请求提交内容类型
    pi_request_data_type = 'application/json'
    # 请求提交内容
    api_request_data_content = '{"name":"hanfeng"}'

    sender = MockDataSender('http://192.168.56.1:9997')

    sender.set_api_path(path).set_api_response(api_response).set_api_request_method(api_request_method).\
        set_api_request_data_content(api_request_data_content).set_api_request_data_type(pi_request_data_type)

    sender.send_mock_data()

    time.sleep(3)

    param = {"name": "hanfeng"}
    res_object = requests.get("http://192.168.56.1:9998/test/go", params=param)
    print(res_object.text)


def mock2():
    # 接口路径
    path = 'orders'
    # 接口响应返回内容
    api_response = '{"orders":[{"id":1,"number":"12"},    {"id":2,"number":"27"}]}'
    # 请求方式
    api_request_method = 'post'
    # 请求提交内容类型
    pi_request_data_type = 'application/xml'
    # 请求提交内容
    api_request_data_content = '''
    <note>
    <to>George</to>
    <from>John</from>
    <heading>Reminder</heading>
    <body>Don't forget the meeting!</body>
    </note>
    '''

    sender = MockDataSender('http://192.168.56.1:9997')

    sender.set_api_path(path).set_api_response(api_response).set_api_request_method(api_request_method).\
        set_api_request_data_content(api_request_data_content).set_api_request_data_type(pi_request_data_type)

    sender.send_mock_data()

    time.sleep(3)

    data = '''
    <note>
    <to>George</to>
    <from>John</from>
    <heading>Reminder</heading>
    <body>Don't forget the meeting!</body>
    </note>
    '''
    res_object = requests.post("http://192.168.56.1:9998/orders", data=data)
    print(res_object.text)

    res_object = sender.clear_mock_data()
    print(res_object.headers)


if __name__ == "__main__":
    # mock2()
    str1 = {"name": "hanfeng"}
    print(json.dumps(str1))
