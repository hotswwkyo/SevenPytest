# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class UserListPage(BasePage):
    """用户列表页面"""
    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_id(self):
            """用户ID输入框"""

            label = '用户ID'
            return self._search_form_input(label)

        @property
        def phone_number(self):
            """手机号输入框"""

            label = '手机号'
            return self._search_form_input(label)

        @property
        def user_alias(self):
            """用户昵称输入框"""

            label = '用户昵称'
            return self._search_form_input(label)

        @property
        def lifecycle(self):
            """生命周期标签"""

            label = '生命周期标签'
            p1 = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div[contains(@class,"ant-form-item-control-wrapper")]'.format(
                label=label)
            p2 = 'div[contains(@class,"ant-form-item-control")]/span[contains(@class,"ant-form-item-children")]/div/div[@role="combobox"]'
            xpath = self.page.join_xpath(p1, p2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_special_attr(self):
            """用户特殊属性标签"""

            label = '用户特殊属性标签'
            p1 = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div[contains(@class,"ant-form-item-control-wrapper")]'.format(
                label=label)
            p2 = 'div[contains(@class,"ant-form-item-control")]/span[contains(@class,"ant-form-item-children")]/div/div[@role="combobox"]'
            xpath = self.page.join_xpath(p1, p2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def usertype(self):
            """用户类型标签"""

            label = '用户类型标签'
            p1 = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div[contains(@class,"ant-form-item-control-wrapper")]'.format(
                label=label)
            p2 = 'div[contains(@class,"ant-form-item-control")]/span[contains(@class,"ant-form-item-children")]/div/div[@role="combobox"]'
            xpath = self.page.join_xpath(p1, p2)
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
        def userlist_table(self):
            """用户列表表格"""

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="用户ID"), 'th/div[normalize-space()="{text}"]'.format(text="手机号"), 'th/div[normalize-space()="{text}"]'.format(text="用户昵称"),
                'th/div[normalize-space()="{text}"]'.format(text="消费总金额"), 'th/div[normalize-space()="{text}"]'.format(text="广告片数量"), 'th/div[normalize-space()="{text}"]'.format(text="订单数量"),
                'th/div[normalize-space()="{text}"]'.format(text="账户启用状态"), 'th/div[normalize-space()="{text}"]'.format(text="操作")
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
            return self.userlist_table.find_element_by_xpath(xpath)

        def all_userlist_table_rows(self):
            """用户列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.userlist_table.find_elements_by_xpath(xpath)

        def userlist_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找用户列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'user_id': 'td[position()=2 and normalize-space()="{text}"]',
                'phone': 'td[position()=3 and normalize-space()="{text}"]',
                'user_alias': 'td[position()=4 and normalize-space()="{text}"]',
                'consume_total_amount': 'td[position()=5]/span[normalize-space()="{text}"]',
                'total_ad': 'td[position()=6 and normalize-space()="{text}"]',
                'total_order': 'td[position()=7 and normalize-space()="{text}"]',
                'user_status': 'td[position()=8]/div[normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.userlist_table.find_elements_by_xpath(xpath)
            else:
                return self.userlist_table.find_element_by_xpath(xpath)

        def userlist_table_row_checkbox(self, rowinfo, match_more=False):
            """ 根据条件 查找指定行，返回行的复选框元素

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            xpath = './td[1]/span/label'
            if match_more:
                checkboxs = []
                for r in self.userlist_table_rows(rowinfo, match_more):
                    checkboxs.append(r.find_element_by_xpath(xpath))
                return checkboxs
            else:
                return self.userlist_table_rows(rowinfo, match_more).find_element_by_xpath(xpath)

        def _userlist_table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    rowinfo: 表格中行的列信息，键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            el_row = self.userlist_table_rows(rowinfo, match_more=False)
            drk = el_row.get_attribute('data-row-key')
            xpath = './ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            return self.userlist_table.find_element_by_xpath(xpath)

        def see_btn(self, rowinfo):
            """查看按钮"""

            name = "查 看"
            return self._userlist_table_row_button(name, rowinfo)

        def edit_btn(self, rowinfo):
            """编辑按钮"""

            name = "编 辑"
            return self._userlist_table_row_button(name, rowinfo)

    class Actions(BasePage.Actions):
        def user_id(self, userid):
            """输入用户id"""

            self.page.elements.user_id.clear()
            self.page.elements.user_id.send_keys(userid)
            return self

        def phone_number(self, number):
            """输入用户id"""

            self.page.elements.phone_number.clear()
            self.page.elements.phone_number.send_keys(number)
            return self

        def user_alias(self, alias):
            """用户昵称"""

            self.page.elements.user_alias.clear()
            self.page.elements.user_alias.send_keys(alias)
            return self

        def lifecycle(self, flag):
            """生命周期标签"""

            self.page.elements.lifecycle.click()
            self.page.elements.sleep(3).dropdown_selectlist(flag).click()
            return self

        def user_special_attr(self, flag):
            """用户特殊属性标签"""

            self.page.elements.user_special_attr.click()
            self.page.elements.sleep(3).dropdown_selectlist(flag).click()
            return self

        def usertype(self, flag):
            """用户类型标签"""

            self.page.elements.usertype.click()
            self.page.elements.sleep(3).dropdown_selectlist(flag).click()
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
                match_more: see self.page.elements.userlist_table_row_checkbox
            """
            cbs = self.page.elements.userlist_table_row_checkbox(rowinfo, match_more=match_more)
            if match_more:
                for cb in cbs:
                    cb.click()
            else:
                cbs.click()
            return self

        def find_userlist_table_rows(self, rowinfo):
            """查找并返回符合条件的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
            """
            return self.page.elements.userlist_table_rows(rowinfo, match_more=True)

        def check_userlist_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    user_id: 用户ID
                    phone: 手机号
                    user_alias: 用户昵称
                    consume_total_amount: 消费总金额
                    total_ad: 广告片数量
                    total_order: 订单数量
                    user_status: 账户启用状态
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_userlist_table_rows, self.page.elements.all_userlist_table_rows, *rows, **checksettings)

        def is_empty_table(self):

            return self.page.elements.no_data_table

        def see(self, rowinfo):
            """点击 查看按钮"""

            self.page.elements.see_btn(rowinfo).click()
            return self

        def edit(self, rowinfo):
            """点击 编辑按钮"""

            self.page.elements.edit_btn(rowinfo).click()
            return self
