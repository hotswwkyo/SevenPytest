import socket

from sevenautotest.utils.SocketTransfer.Common.Handler import TCPServerHandler


class BaseSocketClient(object):

    def __init__(self, ip_addr, ip_port):
        self.host = ip_addr
        self.port = ip_port
        self.packet_number = 0
        self.packet_header_size = 4
        self.recv_default_timeout = 15.0
        self.client = None
        self.handler_client = None
        self.set_packet_header_size()

    def set_packet_header_size(self, size=4):
        self.packet_header_size = size

    def create_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.handler_client = TCPServerHandler(self.client, self.packet_header_size)

    def recv(self):
        message = self.handler_client.recv(buffer_size=64*1024, timeout=self.recv_default_timeout)
        return message

    def send(self, data, encoding='utf-8'):
        self.handler_client.send(data, encoding=encoding)

    def close(self):
        self.client.close()


if __name__ == '__main__':
    c = BaseSocketClient('localhost', 8080)
    c.create_connection()
    c.send('111111')
    c.send('111111')
    c.send('111111')
    c.send('111111')