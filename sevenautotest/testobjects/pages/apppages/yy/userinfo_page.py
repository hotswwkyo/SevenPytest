# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class UserInfoPage(BaseMiniumPage):
    """ 个人资料页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def nickname(self):
            """昵称"""

            s1 = 'mp-cells'
            s2 = 'mp-cell'
            s3 = 'view.weui-cell>view'
            s4 = 'input'
            label = '昵称'
            mpcells = self.page.get_element(s1)
            mpcells.click()
            self.sleep(1)
            el_mpcell_list = mpcells.get_elements(s2)
            el_input = None
            for el_mpcell in el_mpcell_list:
                el_mpcell.click()
                self.sleep(1)
                el_label = el_mpcell.get_element(s3, inner_text=label)
                if el_label:
                    el_input = el_mpcell.get_element(s4)
                    print('el_mpcell.inner_wxml=', el_mpcell.inner_wxml)
                    break
            return el_input

        @property
        def gender(self):
            """性别"""

            s1 = 'mp-cells'
            s2 = 'mp-cell'
            s3 = 'view.weui-cell>view'
            s4 = 'input'
            label = '性别'
            mpcells = self.page.get_element(s1)
            mpcells.click()
            self.sleep(1)
            el_mpcell_list = mpcells.get_elements(s2)
            el_input = None
            for el_mpcell in el_mpcell_list:
                el_mpcell.click()
                self.sleep(1)
                el_label = el_mpcell.get_element(s3, inner_text=label)
                if el_label:
                    el_input = el_mpcell.get_element(s4)
                    print('el_mpcell.inner_wxml=', el_mpcell.inner_wxml)
                    break
            return el_input

        @property
        def save(self):
            """保存按钮"""

            s = 'view>view.button'
            inner_text = '保存'
            return self.page.get_element(s, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def nickname(self, value):
            """设置昵称"""

            self.page.elements.nickname.trigger("input", {"value": value})
            return self

        def male(self, x=1673, y=831):
            """选择男"""

            self.page.elements.gender.click()
            self.sleep(1).click_xy(x, y)
            return self

        def female(self, x=1670, y=782):
            """选择女"""

            self.page.elements.gender.click()
            self.sleep(1).click_xy(x, y)
            return self

        def save(self):
            """点击保存按钮"""

            self.page.elements.save.click()
            return self
