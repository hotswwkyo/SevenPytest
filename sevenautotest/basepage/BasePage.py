# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium import webdriver
from .AbstractBasePage import AbstractBasePage
from sevenautotest import settings
from sevenautotest.utils import TestAssert
from sevenautotest.manager import DriverManager


class BasePage(AbstractBasePage):
    """ """
    @classmethod
    def join_two_xpath(cls, x1, x2):
        """拼接xpath"""

        slash = '/'
        if x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2[1:]
        elif not x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2
        elif x1.endswith(slash) and not x2.startswith(slash):
            return x1 + x2
        else:
            return x1 + slash + x2

    @classmethod
    def join_xpath(cls, *xpath):

        first = xpath[0]
        others = xpath[1:]
        full_xpath = first
        for x in others:
            full_xpath = cls.join_two_xpath(full_xpath, x)
        return full_xpath

    def init(self):

        pass

    def chrome(self, url=None, alias=None, *args, **kwargs):

        executable_path_key = "executable_path"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        if executable_path_key not in kwargs.keys():
            if hasattr(settings, "CHROME_DRIVER_PATH") and settings.CHROME_DRIVER_PATH and isinstance(settings.CHROME_DRIVER_PATH, str):
                kwargs[executable_path_key] = settings.CHROME_DRIVER_PATH
        if 'options' not in kwargs.keys():
            kwargs['options'] = options
        return self.open_browser(DriverManager.CHROME_NAME, url, alias, *args, **kwargs)

    def fail(self, message=""):

        TestAssert.fail(message)

    class Elements(AbstractBasePage.Elements):
        pass

    class Actions(AbstractBasePage.Actions):
        def abstract_check_table(self, fn_find_table_rows, fn_get_all_table_rows, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                fn_find_table_rows: 查找表格行函数，一个参数，接收查询行信息条件的字典， 返回所有匹配的行
                fn_get_all_table_rows: 获取所显示的表格所有行的无参数函数,
                rows: 行信息字典列表，每一行信息是一个字典，[{},...],键定义由具体页面所调用该方法的方法定义
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            actual = 0
            check_total_key = 'check_total'
            not_found_msg = []
            row_times_map = []

            for row in rows:
                el_rows = fn_find_table_rows(row)
                times = len(el_rows)
                if times < 1:
                    sn = len(not_found_msg) + 1
                    msg = '{}.找不到包含以下信息：{}'.format(sn, ', '.join(row.values()))
                    not_found_msg.append(msg)
                row_times_map.append((row, times))
                actual = actual + times
            if not_found_msg:
                self.page.fail('\n'.join(not_found_msg))
            expected = len(rows)
            if check_total_key in checksettings and checksettings[check_total_key]:
                if actual != expected:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(actual, expected))
                total = len(fn_get_all_table_rows())
                if actual != total:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(actual, total))
            return self


if __name__ == "__main__":
    pass
