# -*- coding:utf-8 -*-
import threading
from enum import Enum


class ACCESS(Enum):
    ACCESSIBLE = 1
    FORBIDEEN = 2


class RefusedVisitException(Exception):
    def __str__(self, msg=''):
        string = "__ACCESSIBLE__ is False Can't visit" + msg
        return string


class Container(object):
    __CONTAINER__ = []
    __LOCK = threading.Lock()
    __ACCESSIBLE__ = ACCESS.ACCESSIBLE

    def __init__(self, api_path=None, api_request_method=None, api_request_data_type=None, api_request_data_content=None, api_response=None):
        self.api_path = api_path
        self.api_request_method = api_request_method
        self.api_request_data_type = api_request_data_type
        self.api_request_data_content = api_request_data_content
        self.api_response = api_response

    @classmethod
    def getitem(cls, index, block=False):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            if block:
                with cls.__LOCK:
                    container = cls.__CONTAINER__[index]
            else:
                container = cls.__CONTAINER__[index]
            return container
        else:
            raise RefusedVisitException

    @classmethod
    def len(cls):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            return cls.__CONTAINER__.__len__()
        else:
            raise RefusedVisitException

    @classmethod
    def iter(cls):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            return cls.__CONTAINER__.__iter__()
        else:
            raise RefusedVisitException

    @classmethod
    def append(cls, container):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            with cls.__LOCK:
                if isinstance(container, Container):
                    cls.__CONTAINER__.append(container)
                else:
                    raise TypeError("argv must be Container")
        else:
            raise RefusedVisitException

    @classmethod
    def pop(cls, index):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            with cls.__LOCK:
                container = cls.__CONTAINER__.pop(index)
            return container
        else:
            raise RefusedVisitException

    @classmethod
    def clear(cls):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            with cls.__LOCK:
                cls.__CONTAINER__.clear()
        else:
            raise RefusedVisitException

    @classmethod
    def setState(cls, State):
        if isinstance(State, ACCESS):
            cls.__ACCESSIBLE__ = State
        else:
            raise TypeError('State must be True or False')

    @classmethod
    def getState(cls):
        return cls.__ACCESSIBLE__

    @classmethod
    def empty(cls):
        if cls.__ACCESSIBLE__ == ACCESS.ACCESSIBLE:
            if cls.len() == 0:
                return True
            else:
                return False
        else:
            raise RefusedVisitException


def mock():
    api_path = ['orders']
    # 请求方式
    api_request_method = ['post']
    # 请求提交内容类型
    api_request_data_type = ['application/xml']
    # 请求提交内容
    api_request_data_content = {"name": "hanfeng"}
    # 接口响应返回内容
    api_response = '{"orders":[{"id":1,"number":"12"},{"id":2,"number":"27"}]}'
    content1 = Container(api_path, api_request_method, api_request_data_type, api_request_data_content, api_response)

    Container.setState(True)

    content1.append(content1)

    api_path = ['commands']
    # 请求方式
    api_request_method = ['post']
    # 请求提交内容类型
    api_request_data_type = ['application/xml']
    # 请求提交内容
    api_request_data_content = {"name": "hanfeng"}
    # 接口响应返回内容
    api_response = '{"commands":[{"id":1,"number":"12"},{"id":2,"number":"27"}]}'
    content2 = Container(api_path, api_request_method, api_request_data_type, api_request_data_content, api_response)
    Container.append(content2)

    for content in Container.iter():
        print(content.api_path)

    print("-----------------------------------------------------------")
    Container.pop(-1)

    for content in Container.iter():
        print(content.api_path)

    Container.clear()
    print("-----------------------------------------------------------")
    for content in Container.iter():
        print(content.api_path)


if __name__ == '__main__':
    mock()
