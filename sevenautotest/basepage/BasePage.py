# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium import webdriver
from .AbstractBasePage import AbstractBasePage
from sevenautotest import settings
from sevenautotest.utils import typetools
from sevenautotest.utils import TestAssert
from sevenautotest.manager import DriverManager


class BasePage(AbstractBasePage):
    """ """
    @classmethod
    def join_two_xpath(cls, x1, x2):
        """拼接xpath"""

        slash = '/'
        if x2.strip() == "":
            return x1
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

    @classmethod
    def is_webelement(cls, element):
        return typetools.is_webelement(element)

    def fail(self, message=""):

        TestAssert.fail(message)

    class Elements(AbstractBasePage.Elements):
        pass

    class Actions(AbstractBasePage.Actions):
        def abstract_check_table(self, fn_find_table_rows, fn_get_all_table_rows, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                - fn_find_table_rows: 查找表格行函数，一个参数，接收查询行信息条件的字典， 返回所有匹配的行
                - fn_get_all_table_rows: 获取所显示的表格所有行的无参数函数,
                - rows: 行信息字典列表，每一行信息是一个字典，[{},...],键定义由具体页面所调用该方法的方法定义
                - checksettings: 检查设置变长字典参数，参数如下
                    - check_total: 检查找到的匹配行数是否与预期行数一致 True - 检查 False - 不检查
                    - expected_total_rows: 预期行数，如果不传入该参数则预期的行数取传入行的总数即len(rows)
                    - check_only_has_matching_rows: 检查表格只有匹配的行 True - 检查 False - 不检查
                    - fail_msg: 附加失败消息
                    - show_failed_details: True --- 显示失败详情 False --- 不显示失败详情, 默认为True
                    - turn_page: 控制是否翻页查找, True - 翻页 False - 不翻页， 默认值为False
                    - page_numbers_or_elements: 翻页页码或页码元素构成的列表或元祖，默认为空列表，该参数不为空同时参数turn_page为True才会执行翻页查找
                    - turn_page_wait_time: 翻页等待数据加载时间(秒),无效值或者值小于0则不等待
            """
            is_empty_rows = True
            show_failed_details = checksettings.get("show_failed_details", True)
            fail_msg = checksettings.get("fail_msg", "")
            if not isinstance(fail_msg, (str, bytes)):
                fail_msg = ""
            if isinstance(fail_msg, bytes):
                fail_msg = fail_msg.decode()
            for one in rows:
                if one:
                    is_empty_rows = False
            if is_empty_rows:
                self.page.fail('行信息参数rows不能为空')

            actual = 0
            not_found_msg = []
            row_times_map = []

            # 翻页参数
            turn_page = checksettings.get('turn_page', False)
            turn_page_wait_time = checksettings.get('turn_page_wait_time', None)
            try:
                turn_page_wait_time = int(turn_page_wait_time)
            except Exception:
                turn_page_wait_time = None
            total = 0
            page_numbers_or_elements = checksettings.get('page_numbers_or_elements', [])
            if not isinstance(page_numbers_or_elements, (list, tuple)):
                raise ValueError("param(page_numbers_or_elements) must be a list or tuple composed of page numbers or page elements")
            if turn_page and page_numbers_or_elements:
                befound_info = {}
                for number_or_element in page_numbers_or_elements:
                    self.turn_to_page(number_or_element)
                    if turn_page_wait_time is not None:
                        self.sleep(turn_page_wait_time)
                    for index, row in enumerate(rows):
                        el_rows = fn_find_table_rows(row)
                        counts = len(el_rows)
                        befound_info[index] = befound_info.get(index, 0) + counts
                    if checksettings.get("check_only_has_matching_rows", False):
                        total = total + len(fn_get_all_table_rows())

                for i, row in enumerate(rows):
                    find_times = befound_info.get(i, 0)
                    if find_times < 1:
                        sn = len(not_found_msg) + 1
                        msg = '{}.找不到包含以下信息：{}'.format(sn, ', '.join(row.values()))
                        not_found_msg.append(msg)
                    row_times_map.append((row, find_times))
                    actual = actual + find_times
            else:
                for row in rows:
                    el_rows = fn_find_table_rows(row)
                    times = len(el_rows)
                    if times < 1:
                        sn = len(not_found_msg) + 1
                        msg = '{}.找不到包含以下信息：{}'.format(sn, ', '.join(row.values()))
                        not_found_msg.append(msg)
                    row_times_map.append((row, times))
                    actual = actual + times
                if checksettings.get("check_only_has_matching_rows", False):
                    total = total + len(fn_get_all_table_rows())
            if not_found_msg:
                if show_failed_details:
                    self.page.fail(fail_msg + ': ' + '\n'.join(not_found_msg))
                else:
                    self.page.fail('\n'.join(not_found_msg))

            if checksettings.get("check_total", False):
                expected = checksettings.get("expected_total_rows", len(rows))
                if actual != expected:
                    full_msg = '找到的行数({})和预期的行数({})不相等'.format(actual, expected)
                    if show_failed_details:
                        full_msg = fail_msg + ": " + full_msg
                    self.page.fail(full_msg)
            if checksettings.get("check_only_has_matching_rows", False):
                if actual != total:
                    full_msg = '找到的行数({})和实际页面显示的行数({})不相等'.format(actual, total)
                    if show_failed_details:
                        full_msg = fail_msg + ": " + full_msg
                    self.page.fail(full_msg)
            return self


if __name__ == "__main__":
    pass
