# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class CinemaDetailPage(BasePage):
    """影院详情页面"""
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
        def el_title(self, title='影院详情'):
            """影院详情页标题"""

            xpath = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-header")]/div[normalize-space()="{title}"]'.format(
                title=title)
            return self.page.find_element_by_xpath(xpath)

        def close_btn(self, title='影院详情'):
            """影院详情页面关闭按钮

            Args:
                title: 影院详情页标题
            """

            xpath = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-header")]/div[normalize-space()="{title}"]/following-sibling::button'.format(
                title=title)
            return self.page.find_element_by_xpath(xpath)

        @property
        def baseinfo_table(self):
            """影院详情页 - 基础信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="影院编码"),
                'th/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th/div[normalize-space()="{text}"]'.format(text="启用状态"),
                'th/div[normalize-space()="{text}"]'.format(text="影院图片"),
                'th/div[normalize-space()="{text}"]'.format(text="所属地区"),
                'th/div[normalize-space()="{text}"]'.format(text="具体位置"),
                'th/div[normalize-space()="{text}"]'.format(text="经纬度"),
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_baseinfo_table_rows(self):
            """基础信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.baseinfo_table.find_elements_by_xpath(xpath)

        def baseinfo_table_rows(self, rowinfo, match_more=False):
            """ 根据条件基础信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    cinema_code: 影院编码
                    cinema_name: 影院名称
                    status: 启用状态  启用 | 禁用
                    cinema_img: 影院图片 图片地址
                    belong_area: 所属地区
                    address: 具体位置
                    latitude: 经纬度
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            status_key = 'status'
            tr_xpath = '/ancestor::tr'

            enable_status_name = '启用'
            enable_css_class_name = 'ant-switch-checked'
            enable_attr = ('aria-checked', 'true')

            cols = {
                'cinema_code': 'td[position()=1 and normalize-space()="{text}"]',
                'cinema_name': 'td[position()=2 and normalize-space()="{text}"]',
                status_key: 'td[position()=3]/div/button[contains(@class,"ant-switch")]',
                'cinema_img': 'td[position()=4]/div/img[@src="{text}"]',
                'belong_area': 'td[position()=5]/div[normalize-space()="{text}"]',
                'address': 'td[position()=6 and normalize-space()="{text}"]',
                'latitude': 'td[position()=7]/div[normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    if k in [status_key]:
                        col_xpaths.append(v)
                    else:
                        col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)

            el_rows = self.baseinfo_table.find_elements_by_xpath(xpath)
            match_el_rows = []
            if status_key in rowinfo:
                sv = rowinfo[status_key]
                s_xpath = self.page.join_xpath('./', cols[status_key])

                for el_row in el_rows:
                    el_status_btn = el_row.find_element_by_xpath(s_xpath)
                    is_has_enable_class = el_status_btn.get_attribute('class').find(enable_css_class_name) != -1
                    is_has_enable_attr = el_status_btn.get_attribute(enable_attr[0]) == enable_attr[1]

                    if sv == enable_status_name:
                        if is_has_enable_attr and is_has_enable_class:
                            match_el_rows.append(el_row)
                    else:
                        if not is_has_enable_class or not is_has_enable_attr:
                            match_el_rows.append(el_row)
            else:
                match_el_rows = el_rows
            if match_more:
                return match_el_rows
            else:
                if len(match_el_rows) <= 0:
                    message = "{} with locator '{}' not found".format('xpath', xpath)
                    self.page.raise_no_such_element_exc(message)
                return match_el_rows[0]

        @property
        def no_data_of_baseinfo_table(self):
            """基础信息表格提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.baseinfo_table.find_element_by_xpath(xpath)

        @property
        def contacts_table(self):
            """联系人信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="姓名"),
                'th/div[normalize-space()="{text}"]'.format(text="电话"),
                'th/div[normalize-space()="{text}"]'.format(text="QQ"),
                'th/div[normalize-space()="{text}"]'.format(text="微信"),
                'th/div[normalize-space()="{text}"]'.format(text="邮箱"),
                'th/div[normalize-space()="{text}"]'.format(text="账号状态"),
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_contacts_table_rows(self):
            """联系人信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.contacts_table.find_elements_by_xpath(xpath)

        def contacts_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找联系人信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    name: 姓名
                    phone: 电话
                    qq: QQ
                    wx: 微信
                    email: 有效
                    status: 账号状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'name': 'td[position()=1]/span[normalize-space()="{text}"]',
                'phone': 'td[position()=2 and normalize-space()="{text}"]',
                'qq': 'td[position()=3 and normalize-space()="{text}"]',
                'wx': 'td[position()=3 and normalize-space()="{text}"]',
                'email': 'td[position()=3 and normalize-space()="{text}"]',
                'status': 'td[position()=3 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = self.page.join_xpath(p1, p2)
            if match_more:
                return self.contacts_table.find_elements_by_xpath(xpath)
            else:
                return self.contacts_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_contacts_table(self):
            """ 联系人信息表提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.contacts_table.find_element_by_xpath(xpath)

        @property
        def halllist_table(self):
            """影厅信息列表表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="影厅名称"),
                'th/div[normalize-space()="{text}"]'.format(text="影厅类型"),
                'th/div[normalize-space()="{text}"]'.format(text="签约周期"),
                'th/div[normalize-space()="{text}"]'.format(text="签约时长"),
                'th/div[normalize-space()="{text}"]'.format(text="POS影厅名称"),
                'th/div[normalize-space()="{text}"]'.format(text="POS影厅编码"),
                'th/div[normalize-space()="{text}"]'.format(text="影厅状态"),
                'th/div[normalize-space()="{text}"]'.format(text="每秒价格"),
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_halllist_table_rows(self):
            """影厅信息列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.halllist_table.find_elements_by_xpath(xpath)

        def halllist_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找影厅信息列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_time: 签约时长
                    pos_hall_name: POS影厅名称
                    pos_hall_number: POS影厅编码
                    status: 影厅状态
                    price: 每秒价格
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'hall_name': 'td[position()=1 and normalize-space()="{text}"]',
                'hall_type': 'td[position()=2 and normalize-space()="{text}"]',
                'sign_cycle': 'td[position()=3]/div[normalize-space()="{text}"]',
                'sign_time': 'td[position()=4]/div[normalize-space()="{text}"]',
                'pos_hall_name': 'td[position()=5 and normalize-space()="{text}"]',
                'pos_hall_number': 'td[position()=6 and normalize-space()="{text}"]',
                'status': 'td[position()=7 and normalize-space()="{text}"]',
                'price': 'td[position()=8 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.halllist_table.find_elements_by_xpath(xpath)
            else:
                return self.halllist_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_halllist_table(self):
            """广告片记录提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.halllist_table.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def close(self):
            """退出详情页"""

            self.page.elements.close_btn().click()
            return self

        def find_baseinfo_table_rows(self, rowinfo):
            """ 根据条件 查找基础信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    cinema_code: 影院编码
                    cinema_name: 影院名称
                    status: 启用状态  启用 | 禁用
                    cinema_img: 影院图片 图片地址
                    belong_area: 所属地区
                    address: 具体位置
                    latitude: 经纬度
            """

            return self.page.elements.baseinfo_table_rows(rowinfo, match_more=True)

        def is_empty_baseinfo_table(self):
            """基础信息表是否为空"""

            return self.page.elements.no_data_of_baseinfo_table

        def check_baseinfo_table(self, rowinfo, expected_total=None):
            """ 检查基础信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    cinema_code: 影院编码
                    cinema_name: 影院名称
                    status: 启用状态  启用 | 禁用
                    cinema_img: 影院图片 图片地址
                    belong_area: 所属地区
                    address: 具体位置
                    latitude: 经纬度
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_baseinfo_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的基础信息：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_baseinfo_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self

        def find_contacts_table_rows(self, rowinfo):
            """ 根据条件 查找联系人信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    name: 姓名
                    phone: 电话
                    qq: QQ
                    wx: 微信
                    email: 有效
                    status: 账号状态
            """

            return self.page.elements.contacts_table_rows(rowinfo, match_more=True)

        def is_empty_contacts_table(self):
            """联系人信息表是否为空"""

            return self.page.elements.no_data_of_contacts_table

        def check_contacts_table(self, rowinfo, expected_total=None):
            """ 检查联系人信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    name: 姓名
                    phone: 电话
                    qq: QQ
                    wx: 微信
                    email: 有效
                    status: 账号状态
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_contacts_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的联系人：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_contacts_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self

        def find_halllist_table_rows(self, rowinfo):
            """ 根据条件 查找影厅列表信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_time: 签约时长
                    pos_hall_name: POS影厅名称
                    pos_hall_number: POS影厅编码
                    status: 影厅状态
                    price: 每秒价格
            """

            return self.page.elements.halllist_table_rows(rowinfo, match_more=True)

        def is_empty_halllist_table(self):
            """影厅列表信息表是否为空"""

            return self.page.elements.no_data_of_halllist_table

        def check_halllist_table(self, rowinfo, expected_total=None):
            """ 检查影厅列表信息表格

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    hall_name: 影厅名称
                    hall_type: 影厅类型
                    sign_cycle: 签约周期
                    sign_time: 签约时长
                    pos_hall_name: POS影厅名称
                    pos_hall_number: POS影厅编码
                    status: 影厅状态
                    price: 每秒价格
                expected_total 预期行数, 整数则检查行数是否相等
            """

            find_rows = self.find_halllist_table_rows(rowinfo)
            total_find_rows = len(find_rows)
            if total_find_rows < 1:
                self.page.fail('找不到包含以下信息的影厅：{}'.format(', '.join(rowinfo.values())))

            if expected_total and isinstance(expected_total, int):
                all_rows = self.page.elements.all_halllist_table_rows
                total_all_rows = len(all_rows)

                if total_find_rows != expected_total:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(total_find_rows, expected_total))

                if total_find_rows != total_all_rows:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(total_find_rows, total_all_rows))
            return self
