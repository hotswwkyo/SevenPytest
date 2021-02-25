import logging
import os
import socket
from .Common.Handler import TCPServerHandler


BASE_DIR = os.getcwd()
DATE_FORMAT = "%m/%d/%Y %H:%M:%S"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=BASE_DIR + os.sep + "log" + os.sep + "record.log", filemode="a", format=LOG_FORMAT,
                    level=logging.DEBUG, datefmt=DATE_FORMAT)



class BaseSocketServer(object):

    def __init__(self, ip_addr='localhost', ip_port=8080):
        self.host = ip_addr
        self.port = ip_port
        self.packet_number = 0
        self.packet_header_size = 4
        self.recv_default_timeout = 15.0
        self.client_connection = None
        self.client_address = None
        self.handler_server = None
        self.set_packet_header_size()
        self.__init_server(client_num=5)

    def set_packet_header_size(self, size=4):
        self.packet_header_size = size

    def __init_server(self, client_num=5):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(client_num)

    def run(self):
        self.client_connection, self.client_address = self.server.accept()
        self.handler_server = TCPServerHandler(self.client_connection, self.packet_header_size)

    def recv(self):
        message = self.handler_server.recv(buffer_size=64*1024, timeout=self.recv_default_timeout)
        return message

    def send(self, data, encoding='utf-8'):
        self.handler_server.send(data, encoding=encoding)


if __name__ == '__main__':
    s = BaseSocketServer('localhost', 8080)
    while True:
        s.run()
        print(s.recv())
