# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class ADListPage(BasePage):
    """广告片列表页面"""
    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def ad_number(self):
            """广告编号输入框"""

            label = '广告编号'
            return self._search_form_input(label)

        @property
        def user_id(self):
            """用户ID"""

            label = '用户ID'
            return self._search_form_input(label)

        @property
        def ad_name(self):
            """广告名称输入框"""

            label = '广告名称'
            return self._search_form_input(label)

        @property
        def save_status(self):
            """存储状态 选择框"""

            label = '存储状态'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//div[@role="combobox"]'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        def dropdown_selectlist(self, opt):
            """下拉列表选择框"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-select-dropdown")]/div[@id]/ul/li[@role="option" and normalize-space()="{opt}"]'.format(opt=opt)
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
        def adlist_table(self):
            """广告片列表表格"""

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="广告编号"), 'th/div[normalize-space()="{text}"]'.format(text="广告名称"), 'th/div[normalize-space()="{text}"]'.format(text="用户ID"),
                'th/div[normalize-space()="{text}"]'.format(text="存储状态"), 'th/div[normalize-space()="{text}"]'.format(text="视频大小"), 'th/div[normalize-space()="{text}"]'.format(text="视频时长"),
                'th/div[normalize-space()="{text}"]'.format(text="投放订单数"), 'th/div[normalize-space()="{text}"]'.format(text="操作")
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            return self.page.find_element_by_xpath(xpath)

        @property
        def all_adlist_table_rows(self):
            """广告片列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.adlist_table.find_elements_by_xpath(xpath)

        @property
        def no_data_table(self):
            """提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.adlist_table.find_element_by_xpath(xpath)

        def adlist_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    user_id: 用户ID
                    ad_status: 存储状态
                    ad_size: 视频大小
                    ad_duration: 视频时长
                    order_count: 投放订单数
                match_more: 控制返回匹配的一行还是多行
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'ad_number': 'td[position()=1 and normalize-space()="{text}"]',
                'ad_name': 'td[position()=2]//span[normalize-space()="{text}"]',
                'user_id': 'td[position()=3]//a[normalize-space()="{text}"]',
                'ad_status': 'td[position()=4 and normalize-space()="{text}"]',
                'ad_size': 'td[position()=5]/div[normalize-space()="{text}"]',
                'ad_duration': 'td[position()=6 and normalize-space()="{text}"]',
                'order_count': 'td[position()=7 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths)
            xpath = self.page.join_xpath(p1, p2, tr_xpath)
            if match_more:
                return self.adlist_table.find_elements_by_xpath(xpath)
            else:
                return self.adlist_table.find_element_by_xpath(xpath)

        def _table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    user_id: 用户ID
                    ad_status: 存储状态
                    ad_size: 视频大小
                    ad_duration: 视频时长
                    order_count: 投放订单数
            """

            el_tr = self.adlist_table_rows(rowinfo)
            drk = el_tr.get_attribute('data-row-key')
            xpath = './ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            return self.adlist_table.find_element_by_xpath(xpath)

        def see_btn(self, rowinfo):
            """查看详情按钮"""

            name = "查看详情"
            return self._table_row_button(name, rowinfo)

    class Actions(BasePage.Actions):
        def ad_number(self, number):
            """输入广告编号"""

            self.page.elements.ad_number.clear()
            self.page.elements.ad_number.send_keys(number)
            return self

        def user_id(self, id):
            """输入用户ID"""

            el = self.page.elements.user_id
            el.clear()
            el.send_keys(id)
            return self

        def ad_name(self, name):
            """输入广告名称"""

            self.page.elements.ad_name.clear()
            self.page.elements.ad_name.send_keys(name)
            return self

        def select_status(self, status):
            """选择 存储状态"""

            self.page.elements.save_status.click()
            self.sleep(2)
            self.page.elements.dropdown_selectlist(status).click()
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
                    ad_number: 广告编号
                    ad_name: 广告名称
                    user_id: 用户ID
                    save_status: 存储状态
            """

            self.page.elements.see_btn(rowinfo).click()
            return self

        def is_empty_table(self):

            return self.page.elements.no_data_table

        def find_adlist_table_rows(self, rowinfo):
            """ 返回找到的匹配行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    user_id: 用户ID
                    ad_status: 存储状态
                    ad_size: 视频大小
                    ad_duration: 视频时长
                    order_count: 投放订单数
            """

            return self.page.elements.adlist_table_rows(rowinfo, match_more=True)

        def check_adlist_table(self, *rows, **checksettings):
            """ 检查广告片列表信息表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    user_id: 用户ID
                    ad_status: 存储状态
                    ad_size: 视频大小
                    ad_duration: 视频时长
                    order_count: 投放订单数
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            actual = 0
            check_total_key = 'check_total'
            not_found_msg = []
            row_times_map = []

            for row in rows:
                el_rows = self.find_adlist_table_rows(row)
                times = len(el_rows)
                if times < 1:
                    sn = len(not_found_msg) + 1
                    msg = '{}.找不到包含以下信息的广告片：{}'.format(sn, ', '.join(row.values()))
                    not_found_msg.append(msg)
                row_times_map.append((row, times))
                actual = actual + times
            if not_found_msg:
                self.page.fail('\n'.join(not_found_msg))
            expected = len(rows)
            if check_total_key in checksettings and checksettings[check_total_key]:
                if actual != expected:
                    self.page.fail('找到的行数({})和预期的行数({})不相等'.format(actual, expected))
                total = len(self.page.elements.all_adlist_table_rows)
                if actual != total:
                    self.page.fail('找到的行数({})和实际页面显示的行数({})不相等'.format(actual, total))
            return self
