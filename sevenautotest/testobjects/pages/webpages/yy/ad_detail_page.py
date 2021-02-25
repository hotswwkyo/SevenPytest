# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class AdDetailPage(BasePage):
    """广告片详情页面 2020-08-28 封装"""
    class Elements(BasePage.Elements):
        def el_title(self, title='广告片详情'):
            """广告位详情页标题"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-drawer-content")]//div[contains(@class, "ant-drawer-header")]/div[contains(@class, "ant-drawer-title") and normalize-space()="{title}"]'.format(
                title=title)
            return self.page.find_element_by_xpath(xpath)

        @property
        def close_btn(self):
            """关闭按钮"""

            xpath = './following-sibling::button'
            return self.el_title().find_element_by_xpath(xpath)

        @property
        def ad_number(self):
            """广告编号"""

            title = '基础信息'
            label = '广告编号'

            p1 = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-drawer-content")]//div[contains(@class, "ant-drawer-body")]'
            p2 = 'div/div[contains(@class, "ant-card-head")]//div[normalize-space()="{title}"]'.format(title=title)
            p3 = '/ancestor::div[contains(@class, "ant-card-head")]/following-sibling::div[contains(@class, "ant-card-body")]//span[contains(@class,"info_title") and normalize-space()="{label}"]/parent::div/parent::div/div[2]/span'.format(
                label=label)
            xpath = self.page.join_xpath(p1, p2, p3)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_id(self):
            """用户ID"""

            title = '基础信息'
            label = '用户ID'

            p1 = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-drawer-content")]//div[contains(@class, "ant-drawer-body")]'
            p2 = 'div/div[contains(@class, "ant-card-head")]//div[normalize-space()="{title}"]'.format(title=title)
            p3 = '/ancestor::div[contains(@class, "ant-card-head")]/following-sibling::div[contains(@class, "ant-card-body")]//span[contains(@class,"info_title") and normalize-space()="{label}"]/parent::div/parent::div/div[4]/a'.format(
                label=label)
            xpath = self.page.join_xpath(p1, p2, p3)
            return self.page.find_element_by_xpath(xpath)

        @property
        def ad_name(self):
            """广告名称"""

            title = '基础信息'
            label = '广告名称'

            p1 = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-drawer-content")]//div[contains(@class, "ant-drawer-body")]'
            p2 = 'div/div[contains(@class, "ant-card-head")]//div[normalize-space()="{title}"]'.format(title=title)
            p3 = '/ancestor::div[contains(@class, "ant-card-head")]/following-sibling::div[contains(@class, "ant-card-body")]//span[contains(@class,"info_title") and normalize-space()="{label}"]/parent::div/parent::div/div[2]/span'.format(
                label=label)
            xpath = self.page.join_xpath(p1, p2, p3)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order_record_table(self):
            """订单记录表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div//div[contains(@class, "ant-drawer-content")]//div[contains(@class, "ant-drawer-body")]/div[contains(@class, "ant-card")]//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="订单编号"),
                'th/div[normalize-space()="{text}"]'.format(text="提交时间"),
                'th/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th/div[normalize-space()="{text}"]'.format(text="影院编码"),
                'th/div[normalize-space()="{text}"]'.format(text="订单状态"),
                'th/div[normalize-space()="{text}"]'.format(text="操作"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(xpath_header, '/ancestor::tr/'.join(cols))
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        @property
        def all_order_record_table_rows(self):
            """订单记录表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.order_record_table.find_elements_by_xpath(xpath)

        def order_record_table_rows(self, rowinfo, match_more=False):
            """ 根据条件查找订单记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'

            cols = {
                'order_number': 'td[position()=1]/div/a[normalize-space()="{text}"]',
                'create_date': 'td[position()=2 and normalize-space()="{text}"]',
                'cinema_name': 'td[position()=3]/div/a[normalize-space()="{text}"]',
                'cinema_code': 'td[position()=4 and normalize-space()="{text}"]',
                'status': 'td[position()=5 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))
            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.order_record_table.find_elements_by_xpath(xpath)
            else:
                return self.order_record_table.find_element_by_xpath(xpath)

        @property
        def no_data_of_order_record_table(self):
            """订单记录表格提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.order_record_table.find_element_by_xpath(xpath)

        def _table_row_button(self, row, name):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                row: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
            """

            el_tr = self.order_record_table_rows(row)
            drk = el_tr.get_attribute('data-row-key')
            xpath = './ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            return self.order_record_table.find_element_by_xpath(xpath)

        def see_order(self, row):
            """ 查看订单按钮

            Args:
                row: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
            """
            name = '查看订单'
            return self._table_row_button(row, name)

        def audit_status(self, row):
            """ 审核状态按钮

            Args:
                row: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
            """
            name = '审核状态'
            return self._table_row_button(row, name)

    class Actions(BasePage.Actions):
        def close(self):
            """点击关闭按钮"""

            self.page.elements.close_btn.click()
            return self

        def ad_number_equals(self, number):
            """检查广告编号"""

            a_number = self.page.elements.ad_number.text
            if a_number != number:
                self.page.fail('实际({})与预期({})不等'.format(a_number, number))
            print(self.page.elements.ad_name.text)
            print(self.page.elements.user_id.text)
            return self

        def user_id_equals(self, user_id):
            """检查广告编号"""

            a_user_id = self.page.elements.user_id.text
            if a_user_id != user_id:
                self.page.fail('实际({})与预期({})不等'.format(a_user_id, user_id))
            return self

        def ad_name_equals(self, name):
            """检查广告编号"""

            a_name = self.page.elements.ad_name.text
            if a_name != name:
                self.page.fail('实际({})与预期({})不等'.format(a_name, name))
            return self

        def find_order_record_table_rows(self, rowinfo):
            """ 根据条件 查找订单记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
            """

            return self.page.elements.order_record_table_rows(rowinfo, match_more=True)

        def is_empty_order_record_table(self):
            """订单记录表是否为空"""

            return self.page.elements.no_data_of_order_record_table

        def check_order_record_table(self, *rows, **checksettings):
            """ 检查订单记录表格

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    order_number: 订单编号
                    create_date: 提交时间
                    cinema_name: 影院名称
                    cinema_code: 影院编码
                    status: 订单状态
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_order_record_table_rows, self.page.elements.all_order_record_table_rows, *rows, **checksettings)

        def see_order(self, row):
            """点击 查看订单"""

            self.page.elements.see_order(row).click()
            return self

        def audit_status(self, row):
            """点击 审核状态"""

            self.page.elements.audit_status(row).click()
            return self
