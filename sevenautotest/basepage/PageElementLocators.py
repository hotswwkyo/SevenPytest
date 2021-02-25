# -*- coding:utf-8 -*-
"""
从excel获取页面元素定位器提供给被装饰的页面的Elements类方法
"""

__version__ = "1.0"
__author__ = "si wen wei"

import os
import inspect
import functools
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.utils.marker import AttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager
from sevenautotest.reader import TestCaseExcelFileReader
from sevenautotest.basepage import BasePage


class PageElementLocators(AttributeManager):
    """从excel获取页面元素定位器提供给被装饰的页面的Elements类方法"""

    UTF_8 = AttributeMarker("utf-8", True, "utf-8 编码")
    FILE_EXT = AttributeMarker(".xlsx", True, "页面元素定位器文件拓展名")
    FILE_DIR_PATH = AttributeMarker(settings.PAGE_ELEMENTS_LOCATORS_ROOT_DIR, True, "页面元素定位器文件默认查找目录路径")
    BLOCK_FLAG = AttributeMarker("页面元素定位器", True, "区块分割标志")

    def __init__(self, file_name=None, file_dir_path=None, file_ext=".xlsx", sheet_name_or_index=0):
        """根据文件名从指定的excel文件读取出元素定位器数据

        @param file_name 元素定位器文件名, 如果不提供则根据被装饰元素方法所属的页面名称作为文件名
        @param file_dir_path 元素定位器文件所在目录路径，如果不提供则settings.PAGE_ELEMENTS_LOCATORS_ROOT_DIR作为文明目录路径
        @param file_ext 页面元素定位器文件拓展名
        @param sheet_index_or_name Excel 工作表索引
        """

        self.file_name = file_name
        self.file_ext = file_ext
        self.file_dir_path = file_dir_path
        self.sheet_name_or_index = sheet_name_or_index

    def _build_file_full_path(self, element_method_instance):

        name = self.file_name
        ext = self.file_ext
        ext = ext if (ext and not helper.is_blank_space(ext)) else self.FILE_EXT
        dir_path = self.file_dir_path if (self.file_dir_path and not helper.is_blank_space(self.file_dir_path)) else self.FILE_DIR_PATH

        if name and not helper.is_blank_space(name):
            full_name = name if name.endswith(ext) else name + ext
        else:
            if isinstance(element_method_instance, BasePage.Elements):
                page_class_name = element_method_instance.page.__class__.__name__
            else:
                raise ValueError("element method instance must isinstance BasePage.Elements, actual: %s" % element_method_instance)
            full_name = page_class_name + ext

        return os.path.join(dir_path, full_name)

    def _get_locators(self, file_path, func_name):

        locators = []
        locators_blocks = TestCaseExcelFileReader(file_path, testcase_block_separators=self.BLOCK_FLAG, sheet_index_or_name=self.sheet_name_or_index).load_testcase_data()
        for block in locators_blocks:
            if block.name == func_name:
                for row in block.datas:
                    line = {}
                    for cell in row:
                        for title, value in cell.items():
                            if title in line.keys():
                                continue
                            else:
                                line[title] = value
                    locators.append(line)
        return locators[0] if len(locators) > 0 else {}

    def __call__(self, func):

        func_name = func.__name__
        argspec = inspect.getfullargspec(func)

        def insert_to_tuple(t, index, value):
            to_list = list(t)
            to_list.insert(index, value)
            t = tuple(to_list)
            return t

        @functools.wraps(func)
        def _call(instance, *args, **kwargs):
            full_path = self._build_file_full_path(instance)
            total_pos_args = len(argspec.args) + (1 if argspec.varargs else 0)
            if total_pos_args > 1:
                args = insert_to_tuple(args, 0, self._get_locators(full_path, func_name))
                return func(instance, *args, **kwargs)
            else:
                return func(instance)

        return _call
