import argparse
import json
import logging
import os
from sqlite3 import Error, OperationalError
from .BaseSocketServer import BaseSocketServer
from .Common.SqliteTool import SqliteTool
from .Common.LogTool import logger
from .Common.SqliteCommonBase import SqliteCommonBase


class SqliteServer(SqliteCommonBase):

    def __init__(self, ip_addr='localhost', ip_port=8080):
        self.socket_server = BaseSocketServer(ip_addr, ip_port)
        self.sqlite_server = None

    def analyze(self):
        msg = "Start....................................."
        logger(msg, level=logging.INFO)
        while True:
            self.socket_server.run()
            sql_msg = self.socket_server.recv()
            sql_json = json.loads(sql_msg)
            sql_type = sql_json[self.REQUEST_SQL_TYPE[0]]
            sql_script = sql_json[self.REQUEST_SQL[0]]
            sql_database_path = sql_json[self.REQUEST_DATABASE[0]]
            try:
                if os.path.exists(sql_database_path):
                    self.init_sqlite(sql_database_path)
                else:
                    raise OperationalError
            except OperationalError:
                result = 'unable to open database file'
                status = 'failed'
                res = self.build_response(status, result)
            else:
                if sql_type == "SELECT":
                    try:
                        result = ''
                        res = self.sqlite_server.select(sql_script)

                        for row in res:
                            logger(str(res), logging.INFO)
                            r = ''
                            for ele in row:
                                r = r + str(ele) + ','
                            r = r[:-1]
                            result = result + r + '\r\n'
                        result = result[:-2]
                        status = 'success'
                    except Error:
                        result = None
                        status = 'failed'
                    res = self.build_response(status, result)
                else:
                    try:
                        result = None
                        status = 'success'
                        self.sqlite_server.execute(sql_script)
                    except Error:
                        result = None
                        status = 'failed'
                    res = self.build_response(status, result)

            logger(res, level=logging.INFO)
            self.socket_server.send(res)

    def init_sqlite(self, sql_database_path):
        self.sqlite_server = SqliteTool()
        self.sqlite_server.init_connection(sql_database_path)
        self.sqlite_server.create_cursor()

    def build_response(self, status, result):
        res = {
            self.RESPONSE_STATUS[0]: status,
            self.RESPONSE_RESULT[0]: result
        }
        return json.dumps(res)

    @staticmethod
    def main():
        ip, port, _ = args_parser()
        server = SqliteServer(ip, port)
        try:
            server.analyze()
        except Exception:
            result = 'Exception happend, please code'
            status = 'failed'
            res = server.build_response(status, result)
            server.socket_server.send(res)


def args_parser():
    """
    parse args
    """
    parser = argparse.ArgumentParser(description="Set address you need")
    parser.add_argument("-a", "--address", type=str, default='localhost',
                        help="Mock data submit port")
    parser.add_argument("-p", "--port", type=int, default=8080,
                        help="Mock test port")
    parser.add_argument("-m", "--comment", type=str, default='',
                        help="Comment")
    args = parser.parse_args()
    return args.address, args.port, args.comment


if __name__ == '__main__':
    SqliteServer.main()
