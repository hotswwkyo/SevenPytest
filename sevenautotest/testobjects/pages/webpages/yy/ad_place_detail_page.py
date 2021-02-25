# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class AdPlaceDetailPage(BasePage):
    """广告位详情页面"""
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
        def el_title(self, title='广告位详情'):
            """广告位详情页标题"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-modal-content")]/div[contains(@class, "ant-modal-header")]/div[contains(@class, "ant-modal-title") and normalize-space()="{title}"]'.format(
                title=title)
            return self.page.find_element_by_xpath(xpath)

        @property
        def cinema_info_table(self):
            """影院信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-modal-content")]/div[contains(@class, "ant-modal-body")]/div[contains(@class, "ant-card")]//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="所在地区"),
                'th/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th/div[normalize-space()="{text}"]'.format(text="影院编码"),
                'th/div[normalize-space()="{text}"]'.format(text="影厅名称"),
                'th/div[normalize-space()="{text}"]'.format(text="影厅类型"),
                'th/div[normalize-space()="{text}"]'.format(text="签约周期"),
                'th/div[normalize-space()="{text}"]'.format(text="签约时长"),
                'th/div[normalize-space()="{text}"]'.format(text="剩余时长"),
                'th/div[normalize-space()="{text}"]'.format(text="每秒价格"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(xpath_header, '/ancestor::tr/'.join(cols))
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_cinema_info_table_rows(self):
            """影院信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.cinema_info_table.find_elements_by_xpath(xpath)

        def cinema_info_table_rows(self, rowinfo, match_more=False):
            """ 根据条件影院信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    belong_area: 所在地区
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_length: 签约时长
                    time_left: 剩余时长
                    price: 每秒价格
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'

            cols = {
                'belong_area': 'td[position()=1]/div[normalize-space()="{text}"]',
                'cinema_name': 'td[position()=2 and normalize-space()="{text}"]',
                'cinema_code': 'td[position()=3 and normalize-space()="{text}"]',
                'hall_name': 'td[position()=4 and normalize-space()="{text}"]',
                'hall_type': 'td[position()=5 and normalize-space()="{text}"]',
                'sign_cycle': 'td[position()=6 and normalize-space()="{text}"]',
                'sign_length': 'td[position()=7 and normalize-space()="{text}"]',
                'time_left': 'td[position()=8 and normalize-space()="{text}"]',
                'price': 'td[position()=9]/div[normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))
            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.cinema_info_table.find_elements_by_xpath(xpath)
            else:
                return self.cinema_info_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_cinema_info_table(self):
            """影院信息表格提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.cinema_info_table.find_element_by_xpath(xpath)

        @property
        def film_table(self):
            """影片信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-modal-content")]/div[contains(@class, "ant-modal-body")]/div[contains(@class, "ant-card")]//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="影片名称"),
                'th/div[normalize-space()="{text}"]'.format(text="影片类型"),
                'th/div[normalize-space()="{text}"]'.format(text="排期时间"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(xpath_header, '/ancestor::tr/'.join(cols))
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_film_table_rows(self):
            """影片信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.film_table.find_elements_by_xpath(xpath)

        def film_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找影片信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    film_name: 影片名称
                    film_type: 影片类型
                    showtime: 排期时间
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'film_name': 'td[position()=1 and normalize-space()="{text}"]',
                'film_type': 'td[position()=2 and normalize-space()="{text}"]',
                'showtime': 'td[position()=3 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.film_table.find_elements_by_xpath(xpath)
            else:
                return self.film_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_film_table(self):
            """影片信息表提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.film_table.find_element_by_xpath(xpath)

        @property
        def position_table(self):
            """占位信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-modal-content")]/div[contains(@class, "ant-modal-body")]/div[contains(@class, "ant-card")]//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="占位编号"),
                'th/div[normalize-space()="{text}"]'.format(text="订单编号"),
                'th/div[normalize-space()="{text}"]'.format(text="广告片名称"),
                'th/div[normalize-space()="{text}"]'.format(text="用户ID"),
                'th/div[normalize-space()="{text}"]'.format(text="占用时段"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(xpath_header, '/ancestor::tr/'.join(cols))
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_position_table_rows(self):
            """占位信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.position_table.find_elements_by_xpath(xpath)

        def position_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找占位信息表格中的行并返回

            todo(siwenwei): 等待显示数据的时候调试

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 占位编号
                    order_number: 订单编号
                    ad_name: 广告片名称
                    user_id: 用户ID
                    zy_shiduan: 占用时段
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'ad_number': 'td[position()=1 and normalize-space()="{text}"]',
                'order_number': 'td[position()=2 and normalize-space()="{text}"]',
                'ad_name': 'td[position()=3]/div[normalize-space()="{text}"]',
                'user_id': 'td[position()=4]/div[normalize-space()="{text}"]',
                'zy_shiduan': 'td[position()=5 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.position_table.find_elements_by_xpath(xpath)
            else:
                return self.position_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_position_table(self):
            """占位信息表格提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.position_table.find_element_by_xpath(xpath)

        def _button(self, name):
            """对话框按钮"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-modal-content")]/div[contains(@class, "ant-modal-footer")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def cancel_btn(self):
            """取消按钮"""

            name = '取 消'
            return self._button(name)

        @property
        def confirm_btn(self):
            """确定按钮"""

            name = '确 定'
            return self._button(name)

    class Actions(BasePage.Actions):
        def cancel(self):
            """点击取消按钮"""

            self.page.elements.cancel_btn.click()
            return self

        def confirm(self):
            """点击确定按钮"""

            self.page.elements.confirm_btn.click()
            return self

        def find_cinema_info_table_rows(self, rowinfo):
            """ 根据条件 查找影院信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    belong_area: 所在地区
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_length: 签约时长
                    time_left: 剩余时长
                    price: 每秒价格
            """

            return self.page.elements.cinema_info_table_rows(rowinfo, match_more=True)

        def is_empty_cinema_info_table(self):
            """影院信息表是否为空"""

            return self.page.elements.no_data_of_cinema_info_table

        def check_cinema_info_table(self, rowinfo, expected_total=None):
            """ 检查影院信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    belong_area: 所在地区
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_length: 签约时长
                    time_left: 剩余时长
                    price: 每秒价格
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_cinema_info_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的影院：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_cinema_info_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self

        def find_film_table_rows(self, rowinfo):
            """ 根据条件 查找影片信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    film_name: 影片名称
                    film_type: 影片类型
                    showtime: 排期时间
            """

            return self.page.elements.film_table_rows(rowinfo, match_more=True)

        def is_empty_film_table(self):
            """影片信息表是否为空"""

            return self.page.elements.no_data_of_film_table

        def check_film_table(self, rowinfo, expected_total=None):
            """ 检查影片信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    film_name: 影片名称
                    film_type: 影片类型
                    showtime: 排期时间
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_film_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的影片：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_film_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self

        def find_position_table_rows(self, rowinfo):
            """ 根据条件 查找占位信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 占位编号
                    order_number: 订单编号
                    ad_name: 广告片名称
                    user_id: 用户ID
                    zy_shiduan: 占用时段
            """

            return self.page.elements.position_table_rows(rowinfo, match_more=True)

        def is_empty_position_table(self):
            """占位信息表是否为空"""

            return self.page.elements.no_data_of_position_table

        def check_position_table(self, rowinfo, expected_total=None):
            """ 检查占位信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 占位编号
                    order_number: 订单编号
                    ad_name: 广告片名称
                    user_id: 用户ID
                    zy_shiduan: 占用时段
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_position_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的占位信息：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_position_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self
