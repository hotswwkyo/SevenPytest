# -*- coding:utf-8 -*-
"""
__description__ = Web服务器模拟工具
__author__ = hanfeng
"""
import argparse
import logging
import re
import urllib.parse
import socket
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import socketserver
import os
from resource.Container import Container, ACCESS, RefusedVisitException

BASE_DIR = os.getcwd()
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FORMAT = "%(asctime)s - %(levelname)s -  %(port)s - %(message)s"
logging.basicConfig(filename=BASE_DIR + os.sep + "log" + os.sep + "record.log", filemode="a", format=LOG_FORMAT, level=logging.INFO, datefmt=DATE_FORMAT)

DefaultAddress = socket.gethostbyname(socket.gethostname())  # !!!REMEMBER TO CHANGE THIS!!!
# DefaultAddress = '127.0.0.1'
NSPort = 8088
DefaultPort = 8061  # Maybe set this to 9000.
NotiferRunningServer = {}
MockRunningServer = {}
MATCH_RESULT = None


def logger(message, extra='', level=logging.ERROR):
    extra_dict = {"port": extra}
    logging.log(level=level, msg=message, extra=extra_dict)


def args_parser():
    """
    parse args
    """
    parser = argparse.ArgumentParser(description="Set port you need")
    parser.add_argument("-s", "--source", type=int, default=8088, help="Mock data submit port")
    parser.add_argument("-p", "--port", type=int, default=8061, help="Mock test port")
    parser.add_argument("-a", "--adress", type=str, default=DefaultAddress, help="Mock test port")
    parser.add_argument("-m", "--comment", type=str, default='', help="Comment")
    args = parser.parse_args()
    return args.source, args.port, args.adress


class WebMockServerRequestHandler(BaseHTTPRequestHandler):
    def my_header(self):
        # GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        # current_time = time.strftime(GMT_FORMAT, time.localtime(time.time()))
        # self.send_header("Server", "openresty")
        # self.send_header("Date", current_time)
        self.send_header("Content-type", "text/xml; charset=UTF-8")
        # self.send_header("Transfer-Encoding", "chunked")
        # self.send_header("Connection", "keep-alive")
        # self.send_header("content-encoding", "gzip")
        self.end_headers()

    def do_HEAD(self):
        global MATCH_RESULT
        if Container.getState():
            if Container.empty():
                msg = "Data container is Empty, Please send message first"
                self.send_error(404)
                logger(msg, extra=self.server.port)
            else:
                for containter in Container.iter():
                    api_path = containter.api_path
                    api_request_method = containter.api_request_method
                    if api_request_method is not None and 'head' in api_request_method:
                        query_path, query_string = urllib.parse.splitquery(self.path)
                        if (api_path is not None) and (api_path == query_path):
                            self.send_response(200)
                            MATCH_RESULT = "SUCCESS"
                            msg = "head response"
                            extra = self.server.server_port
                            logger(msg, extra=extra, level=logging.INFO)
                            return
                    msg = "Request Method not match"
                    MATCH_RESULT = "FAILED"
                    self.send_error(404, message=msg)
                    extra = self.server.server_port
                    logger(msg, extra=extra, level=logging.ERROR)
        else:
            self.send_response(200)
            MATCH_RESULT = "SUCCESS"
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()

    def htmlTestPage(self):
        # var_len =int(self.headers["Content-Length"])
        # post_vars = self.rfile.read(var_len)
        # self.wfile.write("query params is:%s" % post_vars)
        print(self.headers)

    def compareResponseAndType(self, container):
        global MATCH_RESULT
        api_response = container.api_response
        api_request_data_type = container.api_request_data_type
        api_request_data_content = container.api_request_data_content
        if api_request_data_content is not None:
            # 将字符串转换成字典形式比较，忽略空格等影响
            c_len = int(self.headers.get("content-length", None))
            if c_len is None:
                body = self.rfile.read()
            else:
                body = self.rfile.read(c_len)
            postparams = urllib.parse.unquote(body.decode())
            # parse text
            if api_request_data_type is not None:
                if re.search(".*[Jj][Ss][Oo][Nn].*", api_request_data_type[0]):
                    postparams = json.loads(postparams)
                if re.search(".*[Ff][Oo][Rr][Mm].*", api_request_data_type[0]):
                    postparams = urllib.parse.parse_qs(postparams)
                    postparams_new = {}
                    for key, item in postparams.items():
                        postparams_new[key] = item[0]
                    postparams = postparams_new
                if re.search(".*[Xx][Mm][Ll].*", api_request_data_type[0]):
                    postparams = NotifierServerRequestHandler.parse_xml(postparams)

            if api_request_data_content == postparams:
                MATCH_RESULT = "SUCCESS"
                self.send_response(200)
                self.my_header()
                self.wfile.write(api_response[0])
                msg = api_response[0]
                extra = self.server.server_port
                logger(msg, extra=extra, level=logging.INFO)
            else:
                msg = "request data not match"
                self.send_error(404, message=msg)
                extra = self.server.server_port
                logger(msg, extra=extra, level=logging.ERROR)
        else:
            MATCH_RESULT = "SUCCESS"
            self.send_response(200)
            self.my_header()
            self.wfile.write(api_response[0])
            msg = api_response[0]
            extra = self.server.server_port
            logger(msg, extra=extra, level=logging.INFO)

    def postResponse(self):
        global MATCH_RESULT
        if Container.getState() == ACCESS.ACCESSIBLE:
            if Container.empty():
                MATCH_RESULT = "EMPTY"
                msg = "Data container is Empty, Please send message first"
                self.send_error(404)
                logger(msg, extra=self.server.port)
            else:
                for containter in Container.iter():
                    api_path = containter.api_path
                    if api_path is None:
                        api_path = ['/']
                    api_request_method = containter.api_request_method
                    if api_request_method is not None and 'post' in api_request_method:
                        query_path, query_string = urllib.parse.splitquery(self.path)
                        if query_path == api_path[0]:
                            self.compareResponseAndType(containter)
                            return
                        else:
                            MATCH_RESULT = "FAILED"
                            self.send_error(404)
                            msg = "Request Path not match"
                            extra = self.server.server_port
                            logger(msg, extra=extra, level=logging.ERROR)
                            return
                else:
                    MATCH_RESULT = "FAILED"
                    self.send_error(404)
                    msg = "Request Method not match"
                    extra = self.server.server_port
                    logger(msg, extra=extra, level=logging.ERROR)
                    return
        else:
            MATCH_RESULT = "FAILED"
            msg = "Container Can't visited"
            self.send_error(404, message=msg)
            extra = self.server.server_port
            logger(msg, extra=extra, level=logging.ERROR)
            return

    def compareQueryResponseAndType(self, container, query_string):
        global MATCH_RESULT
        api_response = container.api_response

        api_request_data_content = container.api_request_data_content
        if api_request_data_content is not None:
            # 将字符串转换成字典形式比较，忽略空格等影响
            postparams = urllib.parse.unquote(query_string)
            postparams_qs = urllib.parse.parse_qs(postparams)

            if api_request_data_content == postparams_qs:
                MATCH_RESULT = "SUCCESS"
                self.send_response(200)
                self.my_header()
                self.wfile.write(api_response[0])
                msg = api_response[0]
                extra = self.server.server_port
                logger(msg, extra=extra, level=logging.INFO)
            else:
                MATCH_RESULT = "FAILED"
                msg = "Request data not match"
                self.send_error(404, message=msg)
                extra = self.server.server_port
                logger(msg, extra=extra, level=logging.ERROR)
        else:
            MATCH_RESULT = "SUCCESS"
            self.send_response(200)
            self.my_header()
            self.wfile.write(api_response[0])
            msg = api_response[0]
            extra = self.server.server_port
            logger(msg, extra=extra, level=logging.INFO)

    def getResponse(self):
        global MATCH_RESULT
        print("get response.........................................")
        if Container.getState() == ACCESS.ACCESSIBLE:
            if Container.empty():
                MATCH_RESULT = "EMPTY"
                msg = "Data container is Empty, Please send message first"
                self.send_error(404, msg)
                logger(msg, extra=self.server.port)
            else:
                for containter in Container.iter():
                    api_path = containter.api_path
                    if api_path is None:
                        api_path = ['/']
                    api_request_method = containter.api_request_method

                    if api_request_method is not None and 'get' in api_request_method:
                        query_path, query_string = urllib.parse.splitquery(self.path)
                        print(query_string)
                        if query_path == api_path[0]:
                            self.compareQueryResponseAndType(containter, query_string)
                            return
                        else:
                            MATCH_RESULT = "FAILED"
                            msg = "Request Path not match"
                            self.send_error(404, message=msg)
                            extra = self.server.server_port
                            logger(msg, extra=extra, level=logging.ERROR)
                            return
                else:
                    MATCH_RESULT = "FAILED"
                    msg = "Request Method not match"
                    self.send_error(404, message=msg)
                    extra = self.server.server_port
                    logger(msg, extra=extra, level=logging.ERROR)
                    return
        else:
            MATCH_RESULT = "FAILED"
            msg = "Container Can't visited"
            self.send_error(404, message=msg)
            extra = self.server.server_port
            logger(msg, extra=extra, level=logging.ERROR)
            return

    def groupBy(self, iterable, keyfunc):
        """
        keyfunc 	function object
        """
        all = []
        only = []
        groups = []
        for one in iterable:
            by = keyfunc(one)
            all.append((by, one))
            if by in only:
                pass
            else:
                only.append(by)

        for by in only:
            same = []
            for one in all:
                t_key, element = one
                if by == t_key:
                    same.append(element)
            if same:
                groups.append((by, same))

        return groups

    def do_GET(self):
        try:
            """Respond to a GET request."""
            # self.htmlTestPage()
            self.getResponse()
        except Exception as e:
            extra = self.server.server_port
            logger(e, extra=extra, level=logging.ERROR)

    def do_POST(self):
        """Respond to a POST request"""
        try:
            # self.htmlTestPage()
            self.postResponse()
        except Exception as e:
            extra = self.server.server_port
            logger(e, extra=extra, level=logging.ERROR)


class ThreadingHttpMockServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


class WebMockServer(object):
    serverClass = ThreadingHttpMockServer
    handlerClass = WebMockServerRequestHandler

    def __init__(self, host, port):

        if not host:
            host = DefaultAddress
        if port:
            port = port
        else:
            port = DefaultPort
        self.host = host
        self.port = port

    def getid(self, running=MockRunningServer):

        if running:
            already_exist_id = running.keys()
            if already_exist_id:
                max_id = max(already_exist_id, key=lambda x: int(x))
                new_id = int(max_id) + 1
            else:
                new_id = 1
        else:
            new_id = 1
        return new_id

    def create(self):

        address = (self.host, self.port)
        # print time.asctime(), "Server Starts - %s:%s" % (self.host, self.port)
        server = self.serverClass(address, self.handlerClass)
        self.server_id = str(self.getid())
        MockRunningServer[self.server_id] = server

        server.serve_forever()

    def run(self):
        msg = "mock server start..........................................."
        logger(msg, level=logging.INFO)
        threading.Thread(target=self.create).start()

    def close(self):
        server = MockRunningServer[self.server_id]
        server.shutdown()
        server.server_close()
        MockRunningServer.pop(self.server_id)


class NotifierServerRequestHandler(BaseHTTPRequestHandler):
    def deduplication(self, dict_postparams):
        new_dict = {}
        for key, item in dict_postparams.items():
            if len(item) > 1:
                item = list(set(item))
                new_dict[key] = item
            else:
                new_dict[key] = item
        return new_dict

    @staticmethod
    def parse_xml(ele_string):
        root = ET.fromstring(ele_string)
        tags = []
        attrs = []

        def recursion(root):
            tags.append(root.tag)
            attrs.append(root.attrib)
            if root.getchildren() is not None:
                for child in root:
                    recursion(child)

        recursion(root)

        return [tags, attrs]

    @staticmethod
    def parse_tmsrpc(ele_string):
        root = ET.fromstring(ele_string)
        method_name = None
        value = None

        def recursion(root):
            nonlocal value
            nonlocal method_name
            if root.tag == "methodName":
                method_name = root.text
            if root.tag == "value":
                value = root.text
            if root.getchildren() is not None:
                for child in root:
                    recursion(child)

        recursion(root)

        return method_name, json.loads(value)

    @staticmethod
    def parse_xml2(ele_string):
        root = ET.fromstring(ele_string)
        tags = []
        attrs = []
        text = []

        def recursion(root):
            tags.append(root.tag)
            attrs.append(root.attrib)
            re_text = re.findall(r'\w*\.*\w+\.*', root.text)
            if re_text:
                text.append(re_text)
            if root.getchildren() is not None:
                for child in root:
                    recursion(child)

        recursion(root)

        return [tags, attrs, text]

    @staticmethod
    def string_to_dict(dict_postparams):
        container = Container()
        # new_dict = {}
        content_type = dict_postparams.get('api_request_data_type')
        for key, item in dict_postparams.items():
            if key == "api_path":
                new_item = []
                ele = item[0]
                if not ele.startswith("/"):
                    ele = "/" + ele
                elif ele is None:
                    ele = ["/"]
                new_item.append(ele)
                container.api_path = new_item
                # new_dict[key] = new_item
            elif key == "api_request_data_content":
                re_compile = "^\"?(.*)\"?$"
                ele = item[0]
                if content_type is not None:
                    if re.search(".*[Jj][Ss][Oo][Nn].*", content_type[0]):
                        ele = json.loads(ele)

                    elif re.search(".*[Ff][Oo][Rr][Mm].*", content_type[0]):
                        m = re.findall(re_compile, ele)
                        print(m)
                        ele = m[0]
                        ele = urllib.parse.parse_qs(ele)
                        # ele_new = {}
                        # for key, item in ele.items():
                        #     ele_new[key] = item[0]
                        # ele = ele_new

                    elif re.search(".*[Xx][Mm][Ll].*", content_type[0]):
                        ele = NotifierServerRequestHandler.parse_xml(ele)

                    elif re.search(".*[Tt][Mm][Ss][rR][pP][cC].*", content_type[0]):
                        ele = NotifierServerRequestHandler.parse_tmsrpc(ele)

                container.api_request_data_content = ele
            elif key == "api_response":
                # container.api_response = item.encode("utf-8")
                new_b = []
                for b_str in item:
                    new_b.append(b_str.encode("utf-8"))
                    # new_b.append(b_str)
                container.api_response = new_b

            elif key == "api_request_method":
                ele = item[0]
                new_item = [ele.lower()]
                container.api_request_method = new_item
            elif key == "api_request_data_type":
                container.api_request_data_type = item
        return container

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("errorCode", "0")
        self.end_headers()
        response = {"result": MATCH_RESULT}
        self.wfile.write(json.dumps(response).encode("utf-8"))
        # self.htmlTestPage()

    def do_DELETE(self):
        """Respond to a DELETE request."""
        global MATCH_RESULT
        MATCH_RESULT = None
        try:
            Container.clear()
            self.send_response(200)
            self.send_header("errorCode", "0")
            self.end_headers()
            msg = "Clear Container"
            extra = self.server.server_port
            logger(msg, extra=extra, level=logging.INFO)
        except RefusedVisitException:
            self.send_error(404, "Container is REFUSED")

    def do_POST(self):
        try:
            if Container.getState() == ACCESS.ACCESSIBLE:
                query_path, query_string = urllib.parse.splitquery(self.path)
                c_len = int(self.headers.get("content-length", None))
                if c_len is None:
                    body = self.rfile.read()
                else:
                    body = self.rfile.read(c_len)
                # 处理字符串并保存到队列中
                postparams = urllib.parse.unquote(body.decode())
                print(postparams)
                postparams_qs = urllib.parse.parse_qs(postparams)
                container = NotifierServerRequestHandler.string_to_dict(postparams_qs)
                Container.append(container=container)
                self.send_response(200)
                self.send_header("errorCode", "0")
                self.end_headers()
                msg = "Parse Data Complete.................................."
                extra = self.server.server_port
                logger(msg, extra=extra, level=logging.INFO)
            else:
                self.send_response_only(404)
                extra = self.server.server_port
                msg = "Container is Forbidden.................................."
                logger(msg, extra=extra, level=logging.ERROR)
        except Exception as e:
            extra = self.server.server_port
            logger(e, extra=extra, level=logging.ERROR)


class ThreadingHttpNServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


class NotifierServer(object):
    serverClass = ThreadingHttpNServer
    handlerClass = NotifierServerRequestHandler

    def __init__(self, host, port):

        if not host:
            host = DefaultAddress
        if port:
            port = port
        else:
            port = NSPort
        self.host = host
        self.port = port

    def getid(self, running=NotiferRunningServer):

        if running:
            already_exist_id = running.keys()
            if already_exist_id:
                max_id = max(already_exist_id, key=lambda x: int(x))
                new_id = int(max_id) + 1
            else:
                new_id = 1
        else:
            new_id = 1
        return new_id

    def create(self):

        address = (self.host, self.port)
        # print time.asctime(), "Server Starts - %s:%s" % (self.host, self.port)
        server = self.serverClass(address, self.handlerClass)
        self.server_id = str(self.getid())
        NotiferRunningServer[self.server_id] = server

        server.serve_forever()

    def run(self):
        msg = "notify worker start......................................................................"
        logger(msg, level=logging.INFO)
        threading.Thread(target=self.create).start()

    def close(self):
        server = NotiferRunningServer[self.server_id]
        server.shutdown()
        server.server_close()
        NotiferRunningServer.pop(self.server_id)


def main():
    Container.setState(ACCESS.ACCESSIBLE)
    source_port, server_port, server_adress = args_parser()
    print(server_adress)
    notifier_worker = NotifierServer(server_adress, source_port)
    notifier_worker.run()
    mock_worker = WebMockServer(server_adress, server_port)
    mock_worker.run()


if __name__ == '__main__':
    main()
