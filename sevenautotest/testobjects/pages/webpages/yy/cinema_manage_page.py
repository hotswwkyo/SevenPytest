# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class CinemaManagePage(BasePage):
    """影院管理页面"""
    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def cinema_code(self):
            """影院编码输入框"""

            label = '影院编码'
            return self._search_form_input(label)

        @property
        def cinema_name(self):
            """影院名称输入框"""

            label = '影院名称'
            return self._search_form_input(label)

        @property
        def province(self):
            """所属地区省份选择框"""

            label = '所属地区'
            p1 = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div[contains(@class,"ant-form-item-control-wrapper")]'.format(
                label=label)
            p2 = 'div[contains(@class,"ant-form-item-control")]/span[contains(@class,"ant-form-item-children")]/div/div[contains(@class,"ant-select") and position()=1]/div[@role="combobox"]'
            xpath = self.page.join_xpath(p1, p2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def city(self):
            """所属地区城市选择框"""

            label = '所属地区'
            p1 = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div[contains(@class,"ant-form-item-control-wrapper")]'.format(
                label=label)
            p2 = 'div[contains(@class,"ant-form-item-control")]/span[contains(@class,"ant-form-item-children")]/div/div[contains(@class,"ant-select") and position()=2]/div[@role="combobox"]'
            xpath = self.page.join_xpath(p1, p2)
            return self.page.find_element_by_xpath(xpath)

        def dropdown_selectlist(self, opt):
            """下拉列表选择框"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-select-dropdown")]/div[@id]/ul/li[@role="option"]/span[normalize-space()="{opt}"]'.format(opt=opt)
            return self.page.find_element_by_xpath(xpath)

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
        def cinema_table(self):
            """影院列表表格"""

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="影院编码"),
                'th/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th/div[normalize-space()="{text}"]'.format(text="所属地区"),
                'th/div[normalize-space()="{text}"]'.format(text="签约影厅数"),
                'th/div[normalize-space()="{text}"]'.format(text="影院状态"),
                'th/div[normalize-space()="{text}"]'.format(text="操作"),
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        def all_cinema_table_rows(self):
            """影院列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.cinema_table.find_elements_by_xpath(xpath)

        def cinema_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找影院列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    code_number: 影院编码
                    cinema_name: 影院名称
                    belong: 所属地区
                    total: 签约影厅数
                    status: 影院状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'code_number': 'td[position()=1 and normalize-space()="{text}"]',
                'cinema_name': 'td[position()=2 and normalize-space()="{text}"]',
                'belong': 'td[position()=3]/div[normalize-space()="{text}"]',
                'total': 'td[position()=4 and normalize-space()="{text}"]',
                'status': 'td[position()=5]/div[normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.cinema_table.find_elements_by_xpath(xpath)
            else:
                return self.cinema_table.find_element_by_xpath(xpath)

        @property
        def no_data_in_cinema_table(self):
            """订单记录提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.cinema_table.find_element_by_xpath(xpath)

        def _table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    code_number: 影院编码
                    cinema_name: 影院名称
                    belong: 所属地区
                    total: 签约影厅数
                    status: 影院状态
            """
            el_tr = self.cinema_table_rows(rowinfo)
            drk = el_tr.get_attribute('data-row-key')
            btn_xpath = './ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            return self.cinema_table.find_element_by_xpath(btn_xpath)

        def see_btn(self, rowinfo):
            """查看详情按钮"""

            name = "查看详情"
            return self._table_row_button(name, rowinfo)

    class Actions(BasePage.Actions):
        def cinema_code(self, code):
            """输入影院编码"""

            self.page.elements.cinema_code.clear()
            self.page.elements.cinema_code.send_keys(code)
            return self

        def cinema_name(self, name):
            """输入广告名称"""

            self.page.elements.cinema_name.clear()
            self.page.elements.cinema_name.send_keys(name)
            return self

        def province(self, name):
            """输入省"""

            self.page.elements.province.click()
            self.page.elements.sleep(2).dropdown_selectlist(name).click()
            return self

        def city(self, name):
            """输入城市"""

            self.page.elements.city.click()
            self.page.elements.sleep(2).dropdown_selectlist(name).click()
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def see(self, rowinfo):
            """点击 查看详情按钮

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    code_number: 影院编码
                    cinema_name: 影院名称
                    belong: 所属地区
                    total: 签约影厅数
                    status: 影院状态
            """

            self.page.elements.see_btn(rowinfo).click()
            return self

        def find_cinema_table_rows(self, rowinfo):
            """ 根据条件 查找影院列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    code_number: 影院编码
                    cinema_name: 影院名称
                    belong: 所属地区
                    total: 签约影厅数
                    status: 影院状态
            """

            return self.page.elements.cinema_table_rows(rowinfo, match_more=True)

        def check_cinema_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    code_number: 影院编码
                    cinema_name: 影院名称
                    belong: 所属地区
                    total: 签约影厅数
                    status: 影院状态
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_cinema_table_rows, self.page.elements.all_cinema_table_rows, *rows, **checksettings)

        def is_empty_cinema_table(self):
            """广告片记录表是否为空"""

            return self.page.elements.no_data_in_cinema_table
