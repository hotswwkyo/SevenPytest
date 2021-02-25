# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class UserDetailPage(BasePage):
    """用户详情页面"""
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
        @property
        def _user_baseinfo_table_xpath(self):

            xpath = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div/div[contains(@class,"ant-card-body")]/table[contains(@class,"base-info")]'
            return xpath

        @property
        def user_level(self):
            """显示用户等级的元素"""

            prefix = '等级'
            xpath = 'tr/th/img/following-sibling::div'
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            el_divs = self.page.find_elements_by_xpath(xpath)
            el_lv = None
            for el_div in el_divs:
                if el_div.text.strip().startswith(prefix):
                    el_lv = el_div
                    break
            if not el_lv:
                tips = '找不到用户等级元素(xpath="{}")'.format(xpath)
                self.page.raise_no_such_element_exc(tips)

            return el_lv

        @property
        def user_id(self):
            """显示用户ID的元素"""

            label = '用户ID'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_lifecycle(self):
            """显示用户生命周期标签的元素"""

            label = '用户生命周期标签'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_alias(self):
            """显示用户昵称的元素"""

            label = '昵称'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_special_attr(self):
            """显示用户特殊属性标签的元素"""

            label = '用户特殊属性标签'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_phone(self):
            """显示用户手机号的元素"""

            label = '手机号'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def user_kind(self):
            """显示用户类型标签的元素"""

            label = '用户类型标签'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def register_time(self):
            """显示注册时间的元素"""

            label = '注册时间'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def company_alias(self):
            """显示企业运营昵称的元素"""

            label = '企业运营昵称'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def register_channel(self):
            """显示注册入口的元素"""

            label = '注册入口'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def business_license_number(self):
            """显示营业执照编号的元素"""

            label = '营业执照编号'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def status(self):
            """显示账户启用状态的元素"""

            label = '账户启用状态'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def belong_industry(self):
            """显示所属行业的元素"""

            label = '所属行业'
            xpath = 'tr/th/div[normalize-space()="{label}"]/following-sibling::div'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_table_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def statistics_table(self):
            """统计信息表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="最新登陆时间"), 'th/div[normalize-space()="{text}"]'.format(text="最新登陆地区"), 'th/div[normalize-space()="{text}"]'.format(text="最新登陆机型"),
                'th/div[normalize-space()="{text}"]'.format(text="广告片数量"), 'th/div[normalize-space()="{text}"]'.format(text="订单数量"), 'th/div[normalize-space()="{text}"]'.format(text="消费总金额"),
                'th/div[normalize-space()="{text}"]'.format(text="最新消费金额"), 'th/div[normalize-space()="{text}"]'.format(text="最新消费时间")
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        def all_statistics_table_rows(self):
            """统计信息表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.statistics_table.find_elements_by_xpath(xpath)

        def statistics_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找统计信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    latest_login_time: 最新登陆时间
                    latest_login_area: 最新登陆地区
                    latest_login_phone: 最新登陆机型
                    ad_number: 广告片数量
                    order_number: 订单数量
                    total_amount: 消费总金额
                    latest_amount: 最新消费金额
                    latest_time: 最新消费时间
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'

            tr_xpath = '/ancestor::tr'
            cols = {
                'latest_login_time': 'td[position()=1]/span[normalize-space()="{text}"]',  # 最新登陆时间
                'latest_login_area': 'td[position()=2 and normalize-space()="{text}"]',  # 最新登陆地区
                'latest_login_phone': 'td[position()=3 and normalize-space()="{text}"]',  # 最新登陆机型
                'ad_number': 'td[position()=4 and normalize-space()="{text}"]',  # 广告片数量
                'order_number': 'td[position()=5 and normalize-space()="{text}"]',  # 订单数量
                'total_amount': 'td[position()=6]/div[normalize-space()="{text}"]',  # 消费总金额
                'latest_amount': 'td[position()=7 and normalize-space()="{text}"]',  # 最新消费金额
                'latest_time': 'td[position()=8 and normalize-space()="{text}"]',  # 最新消费时间
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.statistics_table.find_elements_by_xpath(xpath)
            else:
                return self.statistics_table.find_element_by_xpath(xpath)

        @property
        def no_data_statistics_table(self):
            """统计信息提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.statistics_table.find_element_by_xpath(xpath)

        @property
        def protocol_table(self):
            """用户协议表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="协议名称"), 'th/div[normalize-space()="{text}"]'.format(text="发布时间"), 'th/div[normalize-space()="{text}"]'.format(text="用户签订协议时间"),
                'th/div[normalize-space()="{text}"]'.format(text="操作")
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        def all_protocol_table_rows(self):
            """用户协议表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.protocol_table.find_elements_by_xpath(xpath)

        def protocol_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找统计信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    name: 协议名称
                    release_time: 发布时间
                    sign_time: 用户签订协议时间
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'

            tr_xpath = '/ancestor::tr'
            cols = {
                'name': 'td[position()=1]/span[normalize-space()="{text}"]',  # 协议名称
                'release_time': 'td[position()=2 and normalize-space()="{text}"]',  # 发布时间
                'sign_time': 'td[position()=3 and normalize-space()="{text}"]',  # 用户签订协议时间
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.protocol_table.find_elements_by_xpath(xpath)
            else:
                return self.protocol_table.find_element_by_xpath(xpath)

        @property
        def no_data_protocol_table(self):
            """统计信息提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.protocol_table.find_element_by_xpath(xpath)

        @property
        def ad_record_table(self):
            """广告片记录表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="广告编号"), 'th/div[normalize-space()="{text}"]'.format(text="广告名称"), 'th/div[normalize-space()="{text}"]'.format(text="视频大小M"),
                'th/div[normalize-space()="{text}"]'.format(text="视频时长S"), 'th/div[normalize-space()="{text}"]'.format(text="投放订单数"), 'th/div[normalize-space()="{text}"]'.format(text="操作")
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        def all_ad_record_table_rows(self):
            """广告片记录表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.ad_record_table.find_elements_by_xpath(xpath)

        def ad_record_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找广告片记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    video_size: 视频大小M
                    video_duration: 视频时长S
                    total_order: 投放订单数
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'

            tr_xpath = '/ancestor::tr'
            cols = {
                'ad_number': 'td[position()=1 and normalize-space()="{text}"]',  # 广告编号
                'ad_name': 'td[position()=2 and normalize-space()="{text}"]',  # 广告名称
                'video_size': 'td[position()=3]/div[normalize-space()="{text}"]',  # 视频大小M
                'video_duration': 'td[position()=4]/div[normalize-space()="{text}"]',  # 视频时长S
                'total_order': 'td[position()=5 and normalize-space()="{text}"]',  # 投放订单数
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.ad_record_table.find_elements_by_xpath(xpath)
            else:
                return self.ad_record_table.find_element_by_xpath(xpath)

        @property
        def no_data_ad_record_table(self):
            """广告片记录提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.ad_record_table.find_element_by_xpath(xpath)

        @property
        def order_record_table(self):
            """订单记录表格"""

            xpath_header = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]/div//table/thead/tr/'

            cols = [
                'th/div[normalize-space()="{text}"]'.format(text="订单编号"),
                'th/div[normalize-space()="{text}"]'.format(text="提交时间"),
                'th/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th/div[normalize-space()="{text}"]'.format(text="广告编号"),
                'th/div[normalize-space()="{text}"]'.format(text="订单金额"),
                'th/div[normalize-space()="{text}"]'.format(text="支付方式"),
                'th/div[normalize-space()="{text}"]'.format(text="订单状态"),
                'th/div[normalize-space()="{text}"]'.format(text="操作"),
            ]
            cols.append('ancestor::table')
            xpath = xpath_header + '/ancestor::tr/'.join(cols)
            el_table = self.page.find_element_by_xpath(xpath)
            self.page.scroll_into_view(el_table)
            return el_table

        def all_order_record_table_rows(self):
            """订单记录表格当前页所有行"""

            xpath = './tbody/tr[@data-row-key]'
            return self.order_record_table.find_elements_by_xpath(xpath)

        def order_record_table_rows(self, rowinfo, match_more=False):
            """ 根据条件 查找订单记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    submit_time: 提交时间
                    cinema_name: 影院名称
                    ad_number: 广告编号
                    order_amount: 订单金额
                    pay_channel: 支付方式
                    order_status: 订单状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            p1 = './tbody/tr/'

            tr_xpath = '/ancestor::tr'
            cols = {
                'order_number': 'td[position()=1 and normalize-space()="{text}"]',  # 订单编号
                'submit_time': 'td[position()=2 and normalize-space()="{text}"]',  # 提交时间
                'cinema_name': 'td[position()=3 and normalize-space()="{text}"]',  # 影院名称
                'ad_number': 'td[position()=4 and normalize-space()="{text}"]',  # 广告编号
                'order_amount': 'td[position()=5 and normalize-space()="{text}"]',  # 订单金额
                'pay_channel': 'td[position()=6]/div/span/[normalize-space()="{text}"]',  # 支付方式
                'order_status': 'td[position()=7]/div/span/[normalize-space()="{text}"]',  # 订单状态
            }
            col_xpaths = []
            for k, v in cols.items():
                if k in rowinfo:
                    col_xpaths.append(v.format(text=rowinfo[k]))

            p2 = "/ancestor::tr/".join(col_xpaths) + tr_xpath
            xpath = p1 + p2
            if match_more:
                return self.order_record_table.find_elements_by_xpath(xpath)
            else:
                return self.order_record_table.find_element_by_xpath(xpath)

        @property
        def no_data_order_record_table(self):
            """订单记录提示无数据的元素"""

            desc = '暂无数据'
            xpath = './parent::div[contains(@class,"ant-table-body")]/following-sibling::div/div[contains(@class,"ant-empty")]/div[contains(@class,"ant-empty-image")]/following-sibling::p[normalize-space()="{desc}"]'.format(
                desc=desc)
            return self.order_record_table.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def user_level_equals(self, level):
            """检查用户等级"""

            lv_text = self.page.elements.user_level.text
            if not lv_text.endswith(str(level)):
                self.page.fail('实际用户{}与预期{}不等'.format(lv_text, level))
            return self

        def user_id_equals(self, userid):
            """检查用户id"""

            a_userid = self.page.elements.user_id.text
            if a_userid.strip() != str(userid):
                self.page.fail('实际ID({})与预期({})不等'.format(a_userid, userid))
            return self

        def user_lifecycle_equals(self, expected):
            """检查用户生命周期"""

            actual = self.page.elements.user_lifecycle.text
            if actual.strip() != expected:
                self.page.fail('用户生命周期({})与预期({})不等'.format(actual, expected))
            return self

        def user_alias_equals(self, alias):
            """检查用户昵称"""

            actual = self.page.elements.user_alias.text
            if actual.strip() != alias:
                self.page.fail('实际用户昵称({})与预期({})不等'.format(actual, alias))
            return self

        def user_special_attr_equals(self, expected):
            """检查用户特殊属性标签"""

            actual = self.page.elements.user_special_attr.text
            if actual.strip() != expected:
                self.page.fail('用户特殊属性标签({})与预期({})不等'.format(actual, expected))
            return self

        def user_phone_equals(self, expected):
            """检查手机号"""

            actual = self.page.elements.user_phone.text
            if actual.strip() != expected:
                self.page.fail('手机号({})与预期({})不等'.format(actual, expected))
            return self

        def user_kind_equals(self, expected):
            """检查用户类型标签"""

            actual = self.page.elements.user_kind.text
            if actual.strip() != expected:
                self.page.fail('用户类型标签({})与预期({})不等'.format(actual, expected))
            return self

        def register_time_equals(self, expected):
            """检查注册时间"""

            actual = self.page.elements.register_time.text
            if actual.strip() != expected:
                self.page.fail('注册时间({})与预期({})不等'.format(actual, expected))
            return self

        def company_alias_equals(self, expected):
            """检查企业运营昵称"""

            actual = self.page.elements.company_alias.text
            if actual.strip() != expected:
                self.page.fail('企业运营昵称({})与预期({})不等'.format(actual, expected))
            return self

        def register_channel_equals(self, expected):
            """检查注册入口"""

            actual = self.page.elements.register_channel.text
            if actual.strip() != expected:
                self.page.fail('注册入口({})与预期({})不等'.format(actual, expected))
            return self

        def business_license_number_equals(self, expected):
            """检查营业执照编号"""

            actual = self.page.elements.business_license_number.text
            if actual.strip() != expected:
                self.page.fail('营业执照编号({})与预期({})不等'.format(actual, expected))
            return self

        def status_equals(self, expected):
            """检查账户启用状态"""

            actual = self.page.elements.status.text
            if actual.strip() != expected:
                self.page.fail('账户启用状态({})与预期({})不等'.format(actual, expected))
            return self

        def belong_industry_equals(self, expected):
            """检查所属行业"""

            actual = self.page.elements.belong_industry.text
            if actual.strip() != expected:
                self.page.fail('所属行业({})与预期({})不等'.format(actual, expected))
            return self

        def find_statistics_table_rows(self, rowinfo):
            """ 根据条件 查找统计信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    latest_login_time: 最新登陆时间
                    latest_login_area: 最新登陆地区
                    latest_login_phone: 最新登陆机型
                    ad_number: 广告片数量
                    order_number: 订单数量
                    total_amount: 消费总金额
                    latest_amount: 最新消费金额
                    latest_time: 最新消费时间
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """

            return self.page.elements.statistics_table_rows(rowinfo, match_more=True)

        def is_empty_statistics_table(self):
            """统计信息表是否为空"""

            return self.page.elements.no_data_statistics_table

        def check_statistics_table(self, *rows, **checksettings):
            """ 检查统计信息表格

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    latest_login_time: 最新登陆时间
                    latest_login_area: 最新登陆地区
                    latest_login_phone: 最新登陆机型
                    ad_number: 广告片数量
                    order_number: 订单数量
                    total_amount: 消费总金额
                    latest_amount: 最新消费金额
                    latest_time: 最新消费时间
                checksettings: 检查设置
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_statistics_table_rows, self.page.elements.all_statistics_table_rows, *rows, **checksettings)

        def find_protocol_table_rows(self, rowinfo):
            """ 根据条件 查找统计信息表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    name: 协议名称
                    release_time: 发布时间
                    sign_time: 用户签订协议时间
            """

            return self.page.elements.protocol_table_rows(rowinfo, match_more=True)

        def is_empty_protocol_table(self):
            """统计信息表是否为空"""

            return self.page.elements.no_data_protocol_table

        def check_protocol_table(self, *rows, **checksettings):
            """ 检查表格

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    name: 协议名称
                    release_time: 发布时间
                    sign_time: 用户签订协议时间
                checksettings: 检查设置
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_protocol_table_rows, self.page.elements.all_protocol_table_rows, *rows, **checksettings)

        def find_ad_record_table_rows(self, rowinfo):
            """ 根据条件 查找广告片记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    video_size: 视频大小M
                    video_duration: 视频时长S
                    total_order: 投放订单数
            """

            return self.page.elements.ad_record_table_rows(rowinfo, match_more=True)

        def is_empty_ad_record_table(self):
            """广告片记录表是否为空"""

            return self.page.elements.no_data_ad_record_table

        def check_ad_record_table(self, *rows, **checksettings):
            """ 检查表格

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    ad_number: 广告编号
                    ad_name: 广告名称
                    video_size: 视频大小M
                    video_duration: 视频时长S
                    total_order: 投放订单数
                checksettings: 检查设置
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_ad_record_table_rows, self.page.elements.all_ad_record_table_rows, *rows, **checksettings)

        def find_order_record_table_rows(self, rowinfo):
            """ 根据条件 查找订单记录表格中的行并返回

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    order_number: 订单编号
                    submit_time: 提交时间
                    cinema_name: 影院名称
                    ad_number: 广告编号
                    order_amount: 订单金额
                    pay_channel: 支付方式
                    order_status: 订单状态
            """

            return self.page.elements.order_record_table_rows(rowinfo, match_more=True)

        def is_empty_order_record_table(self):
            """订单记录表是否为空"""

            return self.page.elements.no_data_order_record_table

        def check_order_record_table(self, *rows, **checksettings):
            """ 检查表格

            Args:
                rows: 行信息字典列表，每一行信息是一个字典，[{},...]，每个字典键定义如下
                    order_number: 订单编号
                    submit_time: 提交时间
                    cinema_name: 影院名称
                    ad_number: 广告编号
                    order_amount: 订单金额
                    pay_channel: 支付方式
                    order_status: 订单状态
                checksettings: 检查设置
                    check_total: 检查总数是否一致开关 True - 检查 False - 不检查
            """

            return self.abstract_check_table(self.find_order_record_table_rows, self.page.elements.all_order_record_table_rows, *rows, **checksettings)
