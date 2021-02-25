import json
import re

from sevenautotest.utils.SocketTransfer.BaseSocketClient import BaseSocketClient
from sevenautotest.utils.SocketTransfer.Common.SqliteCommonBase import SqliteCommonBase


class SqliteClient(SqliteCommonBase):
    def __init__(self, ip_addr='localhost', ip_port=8080):
        super().__init__()
        self.socket_client = BaseSocketClient(ip_addr, ip_port)
        self.reuqest = None

    def build_request(self, database_path, sql, sql_type='SELECT'):
        self.request = json.dumps({
            self.REQUEST_DATABASE[0]: database_path,
            self.REQUEST_SQL[0]: sql,
            self.REQUEST_SQL_TYPE[0]: sql_type
        })
        return self.request

    def send_request(self, request=None):
        if request is None:
            self.socket_client.send(self.request)
        else:
            if not isinstance(request, str):
                raise TypeError("Request must be str")
            self.socket_client.send(request)

    def recv_response(self):
        response = self.socket_client.recv()
        response_dict = json.loads(response)
        return self.extract_response(response_dict)

    def extract_response(self, response):
        if response[self.RESPONSE_STATUS[0]] == "success":
            info_list = []
            info = response[self.RESPONSE_RESULT[0]]
            info_sep = re.compile(r'\r\n')
            info = re.split(info_sep, info)
            for inf in info:
                info_list.append(inf.split(','))
            response[self.RESPONSE_RESULT[0]] = info_list
        return response

    def close(self):
        self.socket_client.close()

    def create(self):
        self.socket_client.create_connection()

    def sqlite_request(self, request=None):
        self.create()
        self.send_request(request)
        response = self.recv_response()
        self.close()
        return response

    @staticmethod
    def main(ip, port):
        database_path = r'/usr/tms/code/tms_server/db/tms.db'
        sql_type = 'SELECT'
        sql = 'SELECT * FROM tms_cpl LIMIT 0,2;'
        client = SqliteClient(ip, port)
        client.build_request(database_path, sql, sql_type)
        response = client.sqlite_request()
        print(response)


if __name__ == '__main__' :
    SqliteClient.main('10.201.15.229', 8989)



