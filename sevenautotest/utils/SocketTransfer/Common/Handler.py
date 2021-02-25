import logging
import re
import socket
import struct
try:
    from sevenautotest.utils.LogTools import logger
except ModuleNotFoundError:
    from Common.LogTool import logger


class TCPServerHandler(object):
    def __init__(self, client_connection, packet_header_size=4):
        self.client_connection = client_connection
        self.packet_header_size = packet_header_size
        self.recv_default_timeout = 10

    def recv(self, buffer_size=64 * 1024, timeout=10):
        if self.client_connection is not None:
            headerSize = self.packet_header_size
            dataBuffer = bytes()
            recv_packets = []
            is_stop_recv = False  # 取出的数据刚好是N个包的数据则停止取数据

            if timeout:
                self.client_connection.settimeout(self.check_and_convert_timeout_to_float(timeout))

            while True:
                if is_stop_recv:
                    break
                try:
                    data = self.client_connection.recv(buffer_size)

                    if data:
                        # 把数据存入缓冲区，类似于push数据
                        dataBuffer += data

                        while True:

                            if len(dataBuffer) < headerSize:
                                tips = "数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer)
                                logger(tips, level=logging.DEBUG)
                                break

                            # 读取包头
                            headPack = struct.unpack('>I', dataBuffer[:headerSize])
                            bodySize = headPack[0]

                            # 分包情况处理，跳出函数继续接收数据
                            if len(dataBuffer) < headerSize + bodySize:
                                tips = "数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize + bodySize)
                                logger(tips, level=logging.DEBUG)
                                break
                            # 读取消息正文的内容
                            bodyContent = dataBuffer[headerSize:headerSize + bodySize]
                            logger(bodyContent, level=logging.DEBUG)
                            recv_packets.append(bodyContent)
                            # 数据处理 --- 显示包序号和包正文大小
                            # self.recv_body_data_handle(bodySize, bodyContent)
                            # 粘包情况的处理
                            nextPackData = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出
                            dataBuffer = nextPackData
                            if len(dataBuffer) == 0:  # 如果刚好是一个包的数据
                                is_stop_recv = True
                                break
                    else:
                        break
                except socket.timeout as timeout_error:
                    tips = "recv %s" % timeout_error.args[0]
                    logger(tips, level=logging.DEBUG)
                    break
            self.client_connection.settimeout(None)

            if len(recv_packets) == 1:
                response = recv_packets[0]
                return response
            else:
                return recv_packets
        else:
            raise ConnectionError("No socket client")

    def send(self, data, encoding='utf-8'):
        length = len(data.encode(encoding))
        pack_format = '>I%ss' % length
        vail_data = struct.pack(pack_format, length, data.encode())
        self.client_connection.sendall(vail_data)

    def check_and_convert_timeout_to_float(self, timeout):
        """如果timeout是无效值则返回默认超时时间"""
        vaild_timeout = self.recv_default_timeout
        if timeout:
            if isinstance(timeout, int):
                vaild_timeout = float(timeout)
            elif isinstance(timeout, float):
                vaild_timeout = timeout
            elif isinstance(timeout, str) and self.isNumber(timeout):
                vaild_timeout = float(timeout)
            else:
                pass

        return vaild_timeout

    def isNumber(self, text):

        number = re.compile(r'^[+]?[0-9]+\.[0-9]+$')
        result = number.match(text)
        if result:
            is_number = True
        else:
            is_number = False

        return is_number
