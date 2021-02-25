import requests

from .sendClient import MockDataSender
import time
import json
import os

BASEDIR = os.getcwd()
DATA_DIR = BASEDIR + '//data//'


def example():
    js_file_path = DATA_DIR + "data1.json"
    with open(js_file_path, encoding='utf-8') as f:
        js_file = json.load(f)
    sender = MockDataSender('http://10.1.31.54:9997')
    sender.clear_mock_data()
    for js_element in js_file:
        # 接口路径
        api_path = js_element["api_path"]
        # 接口响应返回内容
        api_response = json.dumps(js_element["api_response"])
        # print(api_response)
        # 请求方式
        api_request_method = js_element["api_request_method"]
        # 请求提交内容类型
        api_request_data_type = js_element["api_request_data_type"]
        # print(api_request_data_type)
        # 请求提交内容
        api_request_data_content = js_element["api_request_data_content"]
        print(type(api_request_data_content))

        sender.set_api_path(api_path).set_api_response(api_response).set_api_request_method(api_request_method).\
            set_api_request_data_content(api_request_data_content).set_api_request_data_type(api_request_data_type)

        sender.send_mock_data()
    print("+" * 100)

    time.sleep(5)

    param = {"isMod": 1}
    res_object = requests.get("http://10.1.31.54:9994/tmsServer/list", params=param)
    print(res_object.text)


if __name__ == '__main__':
    example()
