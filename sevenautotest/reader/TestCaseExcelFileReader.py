# -*- coding:utf-8 -*-
"""
数据文件读取器
"""
import sys
import xlrd
from sevenautotest.utils import helper
from sevenautotest.utils.marker import ConstAttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

__version__ = "1.0"
__author__ = "si wen wei"


class TestCaseBlock(AttributeManager):
    """
    测试用例块
    块中每行数据定义如下:
    所有行中的第一列是标记列
    第一行:    用例名称信息(标记列的下一列是用例名称列，之后是用例别名列)
    第二行:    用例数据标题
    第三行 开始 每一行都是一组完整的测试数据直至遇见空行或者下一个数据块
    """

    UTF_8 = ConstAttributeMarker("UTF-8", "UTF-8字符编码")
    EMPTY_STRING = ConstAttributeMarker("", "空字符串")
    XL_CELL_EMPTY = ConstAttributeMarker(0, "Python value：empty string ''")
    XL_CELL_TEXT = ConstAttributeMarker(1, "Python value：a Unicode string")
    XL_CELL_NUMBER = ConstAttributeMarker(2, "Python value：float")
    XL_CELL_DATE = ConstAttributeMarker(3, "Python value：float")
    XL_CELL_BOOLEAN = ConstAttributeMarker(4, "Python value：int; 1 means TRUE, 0 means FALSE")
    XL_CELL_ERROR = ConstAttributeMarker(5, "Python value：int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code")
    XL_CELL_BLANK = ConstAttributeMarker(6, "Python value：empty string ''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.")

    NAME_ROW_INDEX = ConstAttributeMarker(0, "例块中名称行索引")
    TITLE_ROW_INDEX = ConstAttributeMarker(1, "用例块中数据标题索引")
    MIN_NUMBER_OF_ROWS = ConstAttributeMarker(3, "用例区域至少需要的行数")

    def __init__(self, flag_column_index=0):
        """
        @param flag_column_index 用例区块内分隔符列索引
        """

        self._rows = []  # [(row index in excel file, row), ...]
        self._flag_column_index = flag_column_index

    @property
    def rows(self):

        return self._rows

    def is_valid(self):
        """校验用例数据块是否符合要求（行数最少包含3行 用例名称 行 , 用例数据标题 行 ,  用例数据标题 行[可以有多行]）"""
        return False if len(self.rows) < self.MIN_NUMBER_OF_ROWS else True

    def is_integer(self, number):

        return number % 1 == 0.0 or number % 1 == 0

    def add_block_rows(self, *block_rows):

        for block_row in block_rows:
            self._rows.append(block_row)

    def get_name_row(self):

        return self.rows[self.NAME_ROW_INDEX][1]

    def _get_name_row_values(self):

        values = []
        for cell in self.get_name_row():

            ctype = cell.ctype
            value = cell.value

            if ctype == self.XL_CELL_TEXT and value.strip() != self.EMPTY_STRING:
                values.append(value)
            elif ctype == self.XL_CELL_NUMBER:
                if self.is_integer(value):
                    values.append(str(int(value)))
                else:
                    values.append(str(value))
            else:
                # raise Warning("用例名称单元格类型必须是文本且不能为空")
                pass
        return values

    @property
    def name_column_index(self):

        return self._flag_column_index + 1

    @property
    def alias_column_index(self):

        return self.name_column_index + 1

    @property
    def testcase_name(self):

        cell_values = self._get_name_row_values()
        return cell_values[self.name_column_index]

    @property
    def testcase_alias(self):

        cell_values = self._get_name_row_values()
        return cell_values[self.alias_column_index]

    def is_empty_string(self, value):

        return value.strip() == self.EMPTY_STRING

    def _do_nothing(self, *objs):
        return objs

    def get_data_titles(self):

        titles = []

        for index, cell in enumerate((self.rows[self.TITLE_ROW_INDEX][1])):
            if index == self._flag_column_index:
                continue

            if cell.ctype == self.XL_CELL_TEXT and not self.is_empty_string(cell.value):
                titles.append((index, cell.value))
            else:
                val = cell.value.decode(self.UTF_8) if isinstance(cell.value, bytes) else cell.value
                self._do_nothing(val)
                # raise Warning("用例名称单元格类型必须是文本类型, 单元格类型(%s)=%s" % (cell.ctype, val))
                break
        return titles

    def get_testdata(self):

        all_row_data = []
        for row_index, item in enumerate(self.rows):
            index_in_excel_file, row = item
            if row_index + 1 >= self.MIN_NUMBER_OF_ROWS:
                one_row_data = []
                for title_cell_index, title in self.get_data_titles():
                    value_cell = row[title_cell_index]
                    if value_cell.ctype == self.XL_CELL_TEXT:
                        value = value_cell.value
                    elif value_cell.ctype == self.XL_CELL_EMPTY or value_cell.ctype == self.XL_CELL_BLANK:
                        value = value_cell.value
                    else:
                        raise Warning("用例(%s)数据单元格(%s行%s列)类型必须是文本类型" % (self.testcase_name, index_in_excel_file + 1, title_cell_index + 1))
                    one_row_data.append({title: value})
                all_row_data.append(one_row_data)
        return all_row_data


class TestCaseData(object):
    def __init__(self, name, alias=""):

        self.name = name
        self.alias = alias
        self.datas = []


class TestCaseExcelFileReader(AttributeManager):

    UTF_8 = ConstAttributeMarker("UTF-8", "UTF-8字符编码")
    EMPTY_STRING = ConstAttributeMarker("", "空字符串")
    XL_CELL_EMPTY = ConstAttributeMarker(0, "Python value：empty string ''")
    XL_CELL_TEXT = ConstAttributeMarker(1, "Python value：a Unicode string")
    XL_CELL_NUMBER = ConstAttributeMarker(2, "Python value：float")
    XL_CELL_DATE = ConstAttributeMarker(3, "Python value：float")
    XL_CELL_BOOLEAN = ConstAttributeMarker(4, "Python value：int; 1 means TRUE, 0 means FALSE")
    XL_CELL_ERROR = ConstAttributeMarker(5, "Python value：int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code")
    XL_CELL_BLANK = ConstAttributeMarker(6, "Python value：empty string ''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.")
    DEFAULT_SHEET_INDEX = ConstAttributeMarker(0, "默认取excel的工作表索引")
    DEFAULT_TESTCASE_BLOCK_SEPARATORS = ConstAttributeMarker("用例名称", "默认用例分割标记")

    def __init__(self, filepath, testcase_block_separators="用例名称", testcase_block_separators_column_index=0, sheet_index_or_name=0):
        """
        @param filename – 要打开的电子表格文件的路径。
        @param testcase_block_separators - 用例分割标记
        @param data_start_column_index - 用例分割标记列索引
        """
        self.filepath = filepath
        self.testcase_block_separators = testcase_block_separators if (isinstance(testcase_block_separators, str) and testcase_block_separators) else self.DEFAULT_TESTCASE_BLOCK_SEPARATORS
        self.testcase_block_separators_column_index = testcase_block_separators_column_index if helper.is_positive_integer(testcase_block_separators_column_index) else 0
        self.sheet_index_or_name = sheet_index_or_name if helper.is_positive_integer(sheet_index_or_name) else self.DEFAULT_SHEET_INDEX

        self.open()
        self.select_sheet(self.sheet_index_or_name)

    def open(self):

        self.workbook = xlrd.open_workbook(self.filepath)

    @property
    def sheet(self):

        attr_name = "_sheet"
        if not hasattr(self, attr_name):
            raise AttributeError('{} has no attributes: {}'.format(self, attr_name))
        return self._sheet

    def debug(self):

        testcases = self.load_testcase_data()
        print(len(testcases))
        tc = testcases[0]
        for row in tc.datas:
            line = []
            for cell in row:
                for key in cell:
                    line.append(key + " " + str(cell[key]))
            print(" | ".join(line))
        r1 = tc.datas[0]
        print(r1[0].get("路径"))

    def row_len(self, row_index):

        return self._sheet.row_len(row_index)

    def select_sheet(self, sheet_index_or_name):

        if isinstance(sheet_index_or_name, str):
            self.sheet_index_or_name = sheet_index_or_name
            self._sheet = self.workbook.sheet_by_name(sheet_index_or_name)
        elif isinstance(sheet_index_or_name, int):
            self.sheet_index_or_name = sheet_index_or_name
            self._sheet = self.workbook.sheet_by_index(sheet_index_or_name)
        else:
            raise Warning("传入的工作表名称必须是字符串类型，索引必须是整形数值")
        return self.sheet

    def is_blank_cell(self, cell):

        return cell.ctype == self.XL_CELL_EMPTY or cell.ctype == self.XL_CELL_BLANK

    def is_blank_row(self, row_or_index):

        is_blank = True
        if isinstance(row_or_index, int):
            cells = self._sheet.row(row_or_index)
        else:
            cells = row_or_index
        for cell in cells:
            if not self.is_blank_cell(cell):
                is_blank = False
                break
        return is_blank

    def get_row_indexes(self):

        return range(self._sheet.nrows)

    def get_last_row_index(self):

        return max(self.get_row_indexes())

    def get_testcase_blocks(self):
        """解析并获取用例文件中的用例块区域"""

        zero = 0
        block_start_row_index_list = []
        testcase_block_list = []
        for row_index in self.get_row_indexes():
            if (self.row_len(row_index) == zero):
                continue
            first_cell = self._sheet.cell(row_index, self.testcase_block_separators_column_index)
            if first_cell.ctype == self.XL_CELL_TEXT and first_cell.value == self.testcase_block_separators:
                block_start_row_index_list.append(row_index)

        count = len(block_start_row_index_list)
        for i in range(count):
            testcase_block = TestCaseBlock(self.testcase_block_separators_column_index)
            start_row_index = block_start_row_index_list[i]

            next = i + 1  # 下一个元素索引
            if next >= count:
                end_row_index = self.get_last_row_index()
            else:
                block_other_row_indexs = []
                for r_index in self.get_row_indexes():
                    if r_index >= start_row_index and r_index < block_start_row_index_list[next]:
                        block_other_row_indexs.append(r_index)
                end_row_index = max(block_other_row_indexs)

            for this_row_index in self.get_row_indexes():
                if this_row_index >= start_row_index and this_row_index <= end_row_index:
                    one_row = self._sheet.row(this_row_index)
                    if not self.is_blank_row(one_row):
                        testcase_block.add_block_rows((this_row_index, one_row))
            testcase_block_list.append(testcase_block)
        return testcase_block_list

    def load_testcase_data(self):

        testcases = []
        for testcase_block in self.get_testcase_blocks():

            testcase = TestCaseData(testcase_block.testcase_name, testcase_block.testcase_alias)
            testcase.datas = testcase_block.get_testdata()

            if testcase.name.strip() != self.EMPTY_STRING:
                testcases.append(testcase)
        return testcases


if __name__ == "__main__":
    pass
