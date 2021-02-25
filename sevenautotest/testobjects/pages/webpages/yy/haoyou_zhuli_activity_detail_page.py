# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class HaoYouZhuLiActivityDetailPage(BasePage):
    """好友助力活动详情页面"""
    class Elements(BasePage.Elements):
        @property
        def common_prefix_xpath(self):

            xpath = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]'
            return xpath

        @property
        def page_body_xpath(self):

            xpath = '//div[contains(@class, "ant-drawer-body")]'
            return self.page.join_xpath(self.common_prefix_xpath, xpath)

        def _search_form_input(self, label):

            xpath = '//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(self.page.join_xpath(self.page_body_xpath, xpath))

        @property
        def user_number(self):
            """用户编号输入框"""

            label = '用户编号'
            return self._search_form_input(label)

        @property
        def phone_number(self):
            """手机号输入框"""

            label = '手机号'
            return self._search_form_input(label)

        def dropdown_selectlist(self, opt):
            """下拉列表选择框"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-select-dropdown")]/div[@id]/ul/li[@role="option" and normalize-space()="{opt}"]'.format(opt=opt)
            return self.page.find_element_by_xpath(xpath)

        def _search_form_button(self, name):

            xpath = '//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//span[contains(@class,"table-page-search-submitButtons")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(self.page.join_xpath(self.page_body_xpath, xpath))

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
            """活动详情列表表格"""

            xpath_header = '//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="活动编号"),
                'th/div[normalize-space()="{text}"]'.format(text="活动状态"),
                'th/div[normalize-space()="{text}"]'.format(text="活动开始日期"),
                'th/div[normalize-space()="{text}"]'.format(text="活动结束日期"),
                'th/div[normalize-space()="{text}"]'.format(text="实际结束日期"),
                'th/div[normalize-space()="{text}"]'.format(text="助力发起人数"),
                'th/div[normalize-space()="{text}"]'.format(text="活动新增用户数"),
                'th/div[normalize-space()="{text}"]'.format(text="页面参与度数值"),
                'th/div[normalize-space()="{text}"]'.format(text="优惠券领取总数"),
                'th/div[normalize-space()="{text}"]'.format(text="已使用"),
                'th/div[normalize-space()="{text}"]'.format(text="未使用"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(self.page_body_xpath, xpath_header, '/ancestor::tr/'.join(cols))
            return self.page.find_element_by_xpath(xpath)

        @property
        def no_data_activity_table(self):
            """提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.activity_table.find_element_by_xpath(xpath)

        def all_activity_table_rows(self):
            """活动详情列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.activity_table.find_elements_by_xpath(xpath)

        def activity_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找活动详情列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    start_time: 活动开始日期
                    end_time: 活动结束日期
                    real_end_time: 实际结束日期
                    friends_total: 助力发起人数
                    new_add_users: 活动新增用户数
                    page_access_count: 页面参与度数值
                    receive_coupon_total: 优惠券领取总数
                    used: 已使用
                    unuse: 未使用
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'activity_code': 'td[position()=1 and normalize-space()="{text}"]',
                'activity_status': 'td[position()=2 and normalize-space()="{text}"]',
                'start_time': 'td[position()=3 and normalize-space()="{text}"]',
                'end_time': 'td[position()=4 and normalize-space()="{text}"]',
                'real_end_time': 'td[position()=5]//*[normalize-space()="{text}"]',
                'friends_total': 'td[position()=6 and normalize-space()="{text}"]',
                'new_add_users': 'td[position()=7 and normalize-space()="{text}"]',
                'page_access_count': 'td[position()=8 and normalize-space()="{text}"]',
                'receive_coupon_total': 'td[position()=9 and normalize-space()="{text}"]',
                'used': 'td[position()=10 and normalize-space()="{text}"]',
                'unuse': 'td[position()=11 and normalize-space()="{text}"]',
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

        @property
        def friends_table(self):
            """助力好友列表表格"""

            xpath_header = '//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="用户编号"), 'th/div[normalize-space()="{text}"]'.format(text="用户昵称"), 'th/div[normalize-space()="{text}"]'.format(text="手机号"),
                'th/div[normalize-space()="{text}"]'.format(text="当前助力好友数"), 'th/div[normalize-space()="{text}"]'.format(text="优惠券编码"), 'th/div[normalize-space()="{text}"]'.format(text="优惠券折扣"),
                'th/div[normalize-space()="{text}"]'.format(text="首次分享时间")
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(self.page_body_xpath, xpath_header, '/ancestor::tr/'.join(cols))
            return self.page.find_element_by_xpath(xpath)

        @property
        def no_data_friends_table(self):
            """提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.friends_table.find_element_by_xpath(xpath)

        def all_friends_table_rows(self):
            """助力好友列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.friends_table.find_elements_by_xpath(xpath)

        def friends_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找用户列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_number: 用户编号
                    alias: 用户昵称
                    phone: 手机号
                    friends_total: 当前助力好友数
                    coupon_code_number: 优惠券编码
                    discount: 优惠券折扣
                    first_share_time: 首次分享时间
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'user_number': 'td[position()=1 and normalize-space()="{text}"]',
                'alias': 'td[position()=2 and normalize-space()="{text}"]',
                'phone': 'td[position()=3 and normalize-space()="{text}"]',
                'friends_total': 'td[position()=4]//*[normalize-space()="{text}"]',
                'coupon_code_number': 'td[position()=5 and normalize-space()="{text}"]',
                'discount': 'td[position()=6 and normalize-space()="{text}"]',
                'first_share_time': 'td[position()=7 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.friends_table.find_elements_by_xpath(xpath)
            else:
                return self.friends_table.find_element_by_xpath(xpath)

        @property
        def operation_record_table(self):
            """操作记录列表表格"""

            xpath_header = '//div[contains(@class,"ant-card-body")]//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="时间"),
                'th/div[normalize-space()="{text}"]'.format(text="活动编号"),
                'th/div[normalize-space()="{text}"]'.format(text="内容"),
                'th/div[normalize-space()="{text}"]'.format(text="操作人"),
            ]
            cols.append('ancestor::table')
            xpath = self.page.join_xpath(self.page_body_xpath, xpath_header, '/ancestor::tr/'.join(cols))
            return self.page.find_element_by_xpath(xpath)

        @property
        def no_data_operation_record_table(self):
            """提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.operation_record_table.find_element_by_xpath(xpath)

        def all_operation_record_table_rows(self):
            """操作记录列表表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.operation_record_table.find_elements_by_xpath(xpath)

        def operation_record_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找用户列表表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    create_time: 时间
                    activity_code: 活动编号
                    action: 内容
                    operator: 操作人
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'
            tr_xpath = '/ancestor::tr'
            cols = {
                'create_time': 'td[position()=1 and normalize-space()="{text}"]',
                'activity_code': 'td[position()=2 and normalize-space()="{text}"]',
                'action': 'td[position()=3 and normalize-space()="{text}"]',
                'operator': 'td[position()=4 and normalize-space()="{text}"]',
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.operation_record_table.find_elements_by_xpath(xpath)
            else:
                return self.operation_record_table.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def user_number(self, user_id):
            """输入用户编号"""

            self.page.elements.user_number.clear()
            self.page.elements.user_number.send_keys(user_id)
            return self

        def phone_number(self, number):
            """输入手机号"""

            self.page.elements.phone_number.clear()
            self.page.elements.phone_number.send_keys(number)
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def find_activity_table_rows(self, rowinfo):
            """查找并返回符合条件的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                   activity_code: 活动编号
                    activity_status: 活动状态
                    start_time: 活动开始日期
                    end_time: 活动结束日期
                    real_end_time: 实际结束日期
                    friends_total: 助力发起人数
                    new_add_users: 活动新增用户数
                    page_access_count: 页面参与度数值
                    receive_coupon_total: 优惠券领取总数
                    used: 已使用
                    unuse: 未使用
            """
            return self.page.elements.activity_table_rows(rowinfo, match_more=True)

        def check_activity_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    activity_code: 活动编号
                    activity_status: 活动状态
                    start_time: 活动开始日期
                    end_time: 活动结束日期
                    real_end_time: 实际结束日期
                    friends_total: 助力发起人数
                    new_add_users: 活动新增用户数
                    page_access_count: 页面参与度数值
                    receive_coupon_total: 优惠券领取总数
                    used: 已使用
                    unuse: 未使用
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_activity_table_rows, self.page.elements.all_activity_table_rows, *rows, **checksettings)

        def is_empty_activity_table(self):

            return self.page.elements.no_data_activity_table

        def click_friends_table_row(self, rowinfo, match_more=False):
            """根据条件 点击表格中的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_number: 用户编号
                    alias: 用户昵称
                    phone: 手机号
                    friends_total: 当前助力好友数
                    coupon_code_number: 优惠券编码
                    discount: 优惠券折扣
                    first_share_time: 首次分享时间
                match_more: see self.page.elements.activity_table_row_checkbox
            """
            cbs = self.page.elements.friends_table_rows(rowinfo, match_more=match_more)
            if match_more:
                for cb in cbs:
                    cb.click()
            else:
                cbs.click()
            return self

        def find_friends_table_rows(self, rowinfo):
            """查找并返回符合条件的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    user_number: 用户编号
                    alias: 用户昵称
                    phone: 手机号
                    friends_total: 当前助力好友数
                    coupon_code_number: 优惠券编码
                    discount: 优惠券折扣
                    first_share_time: 首次分享时间
            """
            return self.page.elements.friends_table_rows(rowinfo, match_more=True)

        def check_friends_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    user_number: 用户编号
                    alias: 用户昵称
                    phone: 手机号
                    friends_total: 当前助力好友数
                    coupon_code_number: 优惠券编码
                    discount: 优惠券折扣
                    first_share_time: 首次分享时间
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_friends_table_rows, self.page.elements.all_friends_table_rows, *rows, **checksettings)

        def is_empty_friends_table(self):

            return self.page.elements.no_data_friends_table

        def click_operation_record_table_row(self, rowinfo, match_more=False):
            """根据条件 点击表格中的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    create_time: 时间
                    activity_code: 活动编号
                    action: 内容
                    operator: 操作人
                match_more: see self.page.elements.operation_record_table_rows
            """
            cbs = self.page.elements.operation_record_table_rows(rowinfo, match_more=match_more)
            if match_more:
                for cb in cbs:
                    cb.click()
            else:
                cbs.click()
            return self

        def find_operation_record_table_rows(self, rowinfo):
            """查找并返回符合条件的行

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    create_time: 时间
                    activity_code: 活动编号
                    action: 内容
                    operator: 操作人
            """
            return self.page.elements.operation_record_table_rows(rowinfo, match_more=True)

        def check_operation_record_table(self, *rows, **checksettings):
            """ 检查表格是否有指定的行信息

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    create_time: 时间
                    activity_code: 活动编号
                    action: 内容
                    operator: 操作人
                checksettings: 检查设置,
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_operation_record_table_rows, self.page.elements.all_operation_record_table_rows, *rows, **checksettings)

        def is_empty_operation_record_table(self):

            return self.page.elements.no_data_operation_record_table
