# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class MyselfPage(BaseMiniumPage):
    """ 我的页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def userinfo(self):
            """用户信息"""

            selector = 'view>view.user>navigator>view.userinfo>text.userinfo-nickname'
            return self.page.get_element(selector)

        @property
        def my_ad(self):
            """我的广告素材"""

            selector = 'view>view.user>view>navigator>view'
            inner_text = '我的广告素材'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def invoice_title(self):
            """发票抬头"""

            selector = 'view>view.user>view>navigator>view'
            inner_text = '发票抬头'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def my_coupon(self):
            """我的优惠劵"""

            selector = 'view>view.user>view>navigator>view'
            inner_text = '我的优惠劵'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def friend_help(self):
            """好友助力"""

            selector = 'view>view.user>view>navigator>view'
            inner_text = '好友助力'
            return self.page.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def userinfo(self):
            """点击 用户头像进入用户信息页面"""

            self.page.elements.userinfo.click()
            return self

        def my_ad(self):
            """点击 我的广告素材"""

            self.page.elements.my_ad.click()
            return self

        def invoice_title(self):
            """点击 发票抬头"""

            self.page.elements.invoice_title.click()
            return self

        def my_coupon(self):
            """点击 我的优惠劵"""

            self.page.elements.my_coupon.click()
            return self

        def friend_help(self):
            """点击 好友助力"""

            self.page.elements.friend_help.click()
            return self
