import sqlite3 as sq3


class SqliteTool(object):
    def __init__(self):
        self.__SQLITE_CONS__ = {}
        self.__SQLITE_CURS__ = {}
        self.con = None
        self.current_cursor = None
        self.con_index = 0
        self.cur_index = 0

    def record_con_index(self):
        self.con_index += 1

    def record_cur_index(self):
        self.cur_index += 1

    def init_connection(self, db_path, alias=None):
        self.con = sq3.connect(db_path)
        self.record_con_index()
        if alias is None:
            alias = self.con_index
            self.__SQLITE_CONS__[alias] = self.con
        else:
            self.__SQLITE_CONS__[alias] = self.con
        return alias

    def create_cursor(self, con_alias=None, cur_alias=None):
        if len(self.__SQLITE_CONS__) == 0:
            raise IOError('No connection create')
        if con_alias is not None:
            self.con = self.__SQLITE_CONS__[con_alias]
        self.current_cursor = self.con.cursor()
        self.record_cur_index()
        if cur_alias is None:
            cur_alias = self.con_index
            self.__SQLITE_CURS__[cur_alias] = self.current_cursor
        else:
            self.__SQLITE_CURS__[cur_alias] = self.current_cursor

        return self

    def switch_cursor(self, alias=None):
        if len(self.__SQLITE_CURS__) == 0:
            raise IOError('No cursor create')
        self.current_cursor = self.__SQLITE_CURS__[alias]
        return self

    def switch_connection(self, alias=None):
        if len(self.__SQLITE_CONS__) == 0:
            raise IOError('No connection create')
        self.con = self.__SQLITE_CONS__[alias]
        return self

    def select(self, sql, alias=None):
        if alias is None:
            res = self.current_cursor.execute(sql)
        else:
            self.current_cursor = self.__SQLITE_CURS__[alias]
            res = self.current_cursor.execute(sql)
        return res

    def execute(self, sql, alias=None):
        if alias is None:
            res = self.current_cursor.execute(sql)
            self.con.commit()
        else:
            self.current_cursor = self.__SQLITE_CURS__[alias]
            self.con = self.__SQLITE_CONS__[alias]
            res = self.current_cursor.execute(sql)
            self.con.commit()
        return res

    def commit(self, alias=None):
        if alias is None:
            self.con.commit()
        else:
            self.con = self.__SQLITE_CONS__[alias]
            self.con.commit()

    def close(self, alias=None):
        if alias is None:
            self.con.close()
        else:
            self.con = self.__SQLITE_CONS__[alias]
            self.con.close()

    def close_all(self):
        for con in self.__SQLITE_CONS__:
            con.close()
