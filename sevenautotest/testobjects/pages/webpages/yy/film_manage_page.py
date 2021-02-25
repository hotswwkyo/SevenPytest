# -*- coding: utf-8 -*-

import datetime
from sevenautotest.basepage import BasePage
from sevenautotest.testobjects.pages.webpages.yy.calendar_page import CalendarPage

__author__ = "si wen wei"


class FilmManagePage(BasePage):
    """影片管理页面"""
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

    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def film_name(self):
            """影片名称输入框"""

            label = '影片名称'
            return self._search_form_input(label)

        @property
        def film_type(self):
            """影片类型输入框"""

            label = '影片类型'
            return self._search_form_input(label)

        @property
        def showtime(self):
            """上映时间输入框"""

            label = '上映时间'
            return self._search_form_input(label)

        def _search_form_button(self, name):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//span[contains(@class,"table-page-search-submitButtons")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def search_btn(self):
            """查询按钮"""

            return self._search_form_button('查 询')

        @property
        def reset_btn(self):
            """重置按钮"""

            return self._search_form_button('重 置')

        @property
        def film_list_table(self):
            """影片列表表格"""

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="影片名称"),
                'th/div[normalize-space()="{text}"]'.format(text="宣传海报"),
                'th/div[normalize-space()="{text}"]'.format(text="影片类型"),
                'th/div[normalize-space()="{text}"]'.format(text="影片语言"),
                'th/div[normalize-space()="{text}"]'.format(text="上映日期"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(xpath_header, '/ancestor::tr/'.join(cols))
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_film_list_table_rows(self):
            """影片列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.film_list_table.find_elements_by_xpath(xpath)

        @property
        def no_data_of_film_list_table(self):
            """ 影片表提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.film_list_table.find_element_by_xpath(xpath)

        def _table_operator_button(self, name):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-operator")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def sync_film_btn(self):
            """同步影片按钮"""

            return self._table_operator_button('同步影片')

        def film_list_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    film_name: 影片名称
                    poster: 宣传海报图片url地址
                    film_type: 影片类型
                    film_lan: 影片语言
                    showtime: 上映日期
                match_more: 控制返回匹配的一行还是多行
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'film_name': 'td[position()=1 and normalize-space()="{text}"]',
                'poster': 'td[position()=2]/div/img[@src="{text}"]',
                'film_type': 'td[position()=3 and normalize-space()="{text}"]',
                'film_lan': 'td[position()=4 and normalize-space()="{text}"]',
                'showtime': 'td[position()=5 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.film_list_table.find_elements_by_xpath(xpath)
            else:
                return self.film_list_table.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def film_name(self, name):
            """输入影片名称"""

            self.page.elements.film_name.clear()
            self.page.elements.film_name.send_keys(name)
            return self

        def film_type(self, typename):
            """输入影片类型"""

            self.page.elements.film_type.clear()
            self.page.elements.film_type.send_keys(typename)
            return self

        def showtime(self, date, fmt='%Y-%m-%d'):
            """选择上映时间"""

            obj_date = datetime.datetime.strptime(date, fmt)
            year = obj_date.year
            month = obj_date.month
            day = obj_date.day
            self.page.elements.showtime.click()
            self.page.sleep(2)
            cpage = CalendarPage()
            cpage.actions.select_date(year, month, day, fmt=fmt)
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def sync_film(self):
            """点击 同步影片按钮"""

            self.page.elements.sync_film_btn.click()
            return self

        def find_film_list_table_rows(self, rowinfo):
            """返回找到的匹配行

            Args:
                search_rowinfo: 表格中行的列信息，键定义如下
                    film_name: 影片名称
                    poster: 宣传海报图片url地址
                    film_type: 影片类型
                    film_lan: 影片语言
                    showtime: 上映日期
            """
            return self.page.elements.film_list_table_rows(rowinfo, match_more=True)

        def is_empty_film_list_table(self):
            """影片列表信息表是否为空"""

            return self.page.elements.no_data_of_film_list_table

        def check_film_list_table(self, *rows, **checksettings):
            """ 检查影片列表信息表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    film_name: 影片名称
                    poster: 宣传海报图片url地址
                    film_type: 影片类型
                    film_lan: 影片语言
                    showtime: 上映日期
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            actual = 0
            check_total_key = 'check_total'
            not_found_msg = []
            row_times_map = []

            for row in rows:
                el_rows = self.find_film_list_table_rows(row)
                times = len(el_rows)
                if times < 1:
                    sn = len(not_found_msg) + 1
                    msg = '{}.找不到包含以下信息的影片：{}'.format(sn, ', '.join(row.values()))
                    not_found_msg.append(msg)
                row_times_map.append((row, times))
                actual = actual + times
            if not_found_msg:
                self.page.fail('\n'.join(not_found_msg))
            expected = len(rows)
            if check_total_key in checksettings and checksettings[check_total_key]:
                if actual != expected:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(actual, expected))
                total = len(self.page.elements.all_film_list_table_rows)
                if actual != total:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(actual, total))
            return self
