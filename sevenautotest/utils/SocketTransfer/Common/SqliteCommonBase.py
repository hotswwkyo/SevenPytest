class SqliteCommonBase(object):
    REQUEST_DATABASE = ("database_path", "要查询的数据库")
    REQUEST_SQL = ("sql", r"查询语句")
    REQUEST_SQL_TYPE = ("sql_type", r"查询类型 | SELECT | UPDATE\DELETE\INSERT")

    RESPONSE_STATUS = ("status", "查询状态")
    RESPONSE_RESULT = ("result", "查询结果")
