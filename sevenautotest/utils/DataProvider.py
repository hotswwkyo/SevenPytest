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


class DataProvider(AttributeManager):
    """从excel获取数据传递给被装饰方法的第一个位置参数"""

    UTF_8 = AttributeMarker("utf-8", True, "utf-8 编码")
    FILE_EXT = AttributeMarker(".xlsx", True, "数据文件拓展名")
    FILE_DIR_PATH = AttributeMarker(settings.API_DATA_ROOT_DIR, True, "数据文件默认查找目录路径")
    BLOCK_FLAG = AttributeMarker("数据块", True, "区块分割标志")

    def __init__(self, file_name=None, file_dir_path=None, file_ext=".xlsx", sheet_name_or_index=0):
        """根据文件名从指定的excel文件读取出数据

        @param file_name 数据文件名, 被装饰的方法不是实例的方法则必须提供，否则报错，被装饰方法是实例方法，省略则取所属的实例的类名称作为文件名
        @param file_dir_path 数据文件所在目录路径，如果不提供则settings.API_DATA_ROOT_DIR作为文明目录路径
        @param file_ext 数据文件拓展名
        @param sheet_index_or_name Excel 工作表索引(从0开始)
        """

        self.file_name = file_name
        self.file_ext = file_ext
        self.file_dir_path = file_dir_path
        self.sheet_name_or_index = sheet_name_or_index

    def _build_file_full_path(self, method_instance=None):

        name = self.file_name
        ext = self.file_ext
        ext = ext if (ext and not helper.is_blank_space(ext)) else self.FILE_EXT
        dir_path = self.file_dir_path if (self.file_dir_path and not helper.is_blank_space(self.file_dir_path)) else self.FILE_DIR_PATH

        if name and not helper.is_blank_space(name):
            full_name = name if name.endswith(ext) else name + ext
        else:
            if method_instance and method_instance.__class__ and inspect.isclass(method_instance.__class__):
                final_file_name = method_instance.__class__.__name__
            else:
                raise ValueError("Decorator need to pass param(file_name).")
            full_name = final_file_name + ext

        return os.path.join(dir_path, full_name)

    def _get_datas(self, file_path, func_name):

        datas = []
        datas_blocks = TestCaseExcelFileReader(file_path, testcase_block_separators=self.BLOCK_FLAG, sheet_index_or_name=self.sheet_name_or_index).load_testcase_data()
        for block in datas_blocks:
            if block.name == func_name:
                for row in block.datas:
                    line = {}
                    for cell in row:
                        for title, value in cell.items():
                            if title in line.keys():
                                continue
                            else:
                                line[title] = value
                    datas.append(line)
        return datas[0] if len(datas) > 0 else {}

    def __call__(self, func):

        func_name = func.__name__
        argspec = inspect.getfullargspec(func)

        @functools.wraps(func)
        def _call(*args, **kwargs):

            instance = args[0] if len(args) > 0 else None
            method_instance = instance if instance and self.is_method_instance(instance, func_name) else None
            full_path = self._build_file_full_path(method_instance=method_instance)
            new_args = list(args)
            pos_args_len = len(argspec.args)
            pos_varargs_len = 1 if argspec.varargs else 0
            insert_data = False
            insert_pos_index = 0

            if pos_varargs_len < 0:
                if pos_args_len < 0:
                    insert_data = False
                elif pos_args_len < 2:
                    if method_instance:
                        insert_data = False
                    else:
                        insert_data = True
                        insert_pos_index = 0
                else:
                    insert_data = True
                    if method_instance:
                        insert_pos_index = 1
                    else:
                        insert_pos_index = 0
            else:
                insert_data = True
                if method_instance:
                    insert_pos_index = 1
                else:
                    insert_pos_index = 0
            if insert_data:
                new_args.insert(insert_pos_index, self._get_datas(full_path, func_name))
            return func(*tuple(new_args), **kwargs)

        return _call

    def is_method_instance(self, instance, method_name):
        return inspect.ismethod(getattr(instance, method_name))
