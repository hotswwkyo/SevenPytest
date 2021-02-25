# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage
from .calendar_page import CalendarPage

__author__ = "si wen wei"


class HaoYouZhuLiPage(BasePage):
    """好友助力列表页面"""
    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def starttime(self):
            """开始时间输入框"""

            label = '开始时间'
            return self._search_form_input(label)

        @property
        def status(self):
            """活动状态输入框"""

            label = '活动状态'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//div[contains(@class,"ant-select-selection__placeholder")]'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        def dropdown_selectlist(self, opt):
            """下拉列表选择框"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-select-dropdown")]/div[@id]/ul/li[@role="option" and normalize-space()="{opt}"]'.format(opt=opt)
            return self.page.find_element_by_xpath(xpath)

        def _toolbar_button(self, name):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-operator")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def add_activity_btn(self):
            """添加活动"""

            name = "添加活动"
            return self._toolbar_button(name)

        @property
        def log_btn(self):
            """操作日志"""

            name = "操作日志"
            return self._toolbar_button(name)

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
        def activity_table(self):
            """活动列表表格"""

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="活动编号"), 'th/div[normalize-space()="{text}"]'.format(text="活动状态"), 'th/div[normalize-space()="{text}"]'.format(text="活动周期"),
                'th/div[normalize-space()="{text}"]'.format(text="实际结束日期"), 'th/div[normalize-space()="{text}"]'.format(text="助力发起人"), 'th/div[normalize-space()="{text}"]'.format(text="新增用户"),
                'th/div[normalize-space()="{text}"]'.format(text="操作")
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            return self.page.find_element_by_xpath(xpath)

        @property
        def no_data_table(self):
            """提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.activity_table.find_element_by_xpath(xpath)

        def all_activity_table_rows(self):
            """活动列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.activity_table.find_elements_by_xpath(xpath)

        def activity_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找用户列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    activity_cycle: 活动周期
                    real_end_time: 实际结束日期
                    help_sponsors: 助力发起人
                    new_add_users: 新增用户
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'activity_code': 'td[position()=1 and normalize-space()="{text}"]',
                'activity_status': 'td[position()=2]//*[normalize-space()="{text}"]',
                'activity_cycle': 'td[position()=3]//*[normalize-space()="{text}"]',
                'real_end_time': 'td[position()=4]//*[normalize-space()="{text}"]',
                'help_sponsors': 'td[position()=5 and normalize-space()="{text}"]',
                'new_add_users': 'td[position()=6 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.activity_table.find_elements_by_xpath(xpath)
            else:
                return self.activity_table.find_element_by_xpath(xpath)

        def activity_table_row_checkbox(self, rowinfo, match_more=False):
            """ 根据条件 查找指定行，返回行的复选框元素

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    activity_cycle: 活动周期
                    real_end_time: 实际结束日期
                    help_sponsors: 助力发起人
                    new_add_users: 新增用户
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            xpath = './td[1]/span/label'
            if match_more:
                checkboxs = []
                for r in self.activity_table_rows(rowinfo, match_more):
                    checkboxs.append(r.find_element_by_xpath(xpath))
                return checkboxs
            else:
                return self.activity_table_rows(rowinfo, match_more).find_element_by_xpath(xpath)

        def _activity_table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    activity_cycle: 活动周期
                    real_end_time: 实际结束日期
                    help_sponsors: 助力发起人
                    new_add_users: 新增用户
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            el_row = self.activity_table_rows(rowinfo, match_more=False)
            drk = el_row.get_attribute('data-row-key')
            xpath = './ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            return self.activity_table.find_element_by_xpath(xpath)

        def see_btn(self, rowinfo):
            """查看按钮"""

            name = "查 看"
            return self._activity_table_row_button(name, rowinfo)

        def copy_btn(self, rowinfo):
            """复制按钮"""

            name = "复 制"
            return self._activity_table_row_button(name, rowinfo)

        def detail_btn(self, rowinfo):
            """活动详情按钮"""

            name = "活动详情"
            return self._activity_table_row_button(name, rowinfo)

    class Actions(BasePage.Actions):
        def starttime(self, year, month, day):
            """输入开始时间"""

            self.page.elements.starttime.click()
            CalendarPage().actions.sleep(3).select_date(year, month, day)
            return self

        def status(self, name):
            """输入状态"""

            self.page.elements.status.click()
            self.page.elements.sleep(3).dropdown_selectlist(name).click()
            return self

        def add_activity(self):
            """点击添加活动按钮"""

            self.page.elements.add_activity_btn.click()
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def click_row(self, rowinfo, match_more=False):
            """根据条件 点击表格中的行的复选框

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    rowinfo: 表格中行的列信息，键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
                match_more: see self.page.elements.activity_table_row_checkbox
            """
            cbs = self.page.elements.activity_table_row_checkbox(rowinfo, match_more=match_more)
            if match_more:
                for cb in cbs:
                    cb.click()
            else:
                cbs.click()
            return self

        def find_activity_table_rows(self, rowinfo):
            """查找并返回符合条件的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    activity_cycle: 活动周期
                    real_end_time: 实际结束日期
                    help_sponsors: 助力发起人
                    new_add_users: 新增用户
            """
            return self.page.elements.activity_table_rows(rowinfo, match_more=True)

        def check_activity_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    activity_cycle: 活动周期
                    real_end_time: 实际结束日期
                    help_sponsors: 助力发起人
                    new_add_users: 新增用户
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_activity_table_rows, self.page.elements.all_activity_table_rows, *rows, **checksettings)

        def is_empty_table(self):

            return self.page.elements.no_data_table

        def see(self, rowinfo):
            """点击 查看按钮"""

            self.page.elements.see_btn(rowinfo).click()
            return self

        def copy(self, rowinfo):
            """点击 复制按钮"""

            self.page.elements.copy_btn(rowinfo).click()
            return self

        def detail(self, rowinfo):
            """点击 活动详情按钮"""

            self.page.elements.detail_btn(rowinfo).click()
            return self
