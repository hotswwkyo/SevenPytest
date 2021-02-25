# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class OrderPage(BaseMiniumPage):
    """ 订单页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def all_orders(self):
            """全部订单"""

            selector = 'view>view.car>view.header>text'
            inner_text = '全部订单'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def to_be_paid(self):
            """待付款"""

            selector = 'view>view.car>view.header>text'
            inner_text = '待付款'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def to_be_approval(self):
            """待审核"""

            selector = 'view>view.car>view.header>text'
            inner_text = '待审核'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def to_be_run(self):
            """执行中"""

            selector = 'view>view.car>view.header>text'
            inner_text = '执行中'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def to_be_discuss(self):
            """待评价"""

            selector = 'view>view.car>view.header>text'
            inner_text = '待评价'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def tabbar(self):
            """首页下方tab工具栏"""

            selector = '.mp-tabbar'
            return self.page.get_element(selector)

        @property
        def home_tab(self):
            """首页 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "首页"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def ad_tab(self):
            """广告篮 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "广告篮"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def order_tab(self):
            """订单 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "订单"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def my_tab(self):
            """我的 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "我的"
            return self.tabbar.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def all_orders(self):
            """点击全部订单"""

            self.page.elements.all_orders.click()
            return self

        def to_be_paid(self):
            """点击待付款"""

            self.page.elements.to_be_paid.click()
            return self

        def to_be_approval(self):
            """点击待审核"""

            self.page.elements.to_be_approval.click()
            return self

        def to_be_run(self):
            """点击执行中"""

            self.page.elements.to_be_run.click()
            return self

        def to_be_discuss(self):
            """待评价"""

            self.page.elements.to_be_discuss.click()
            return self

        def click_tabbar(self):
            """点击下方标签工具栏"""

            self.page.elements.tabbar.click()
            return self

        def click_home_tab(self):
            """点击下方首页标签"""

            self.page.elements.home_tab.click()
            return self

        def click_ad_tab(self):
            """点击下方广告篮标签"""

            self.page.elements.ad_tab.click()
            return self

        def click_order_tab(self):
            """点击下方订单标签"""

            self.page.elements.order_tab.click()
            return self

        def click_my_tab(self):
            """点击下方我的标签"""

            self.page.elements.my_tab.click()
            return self
