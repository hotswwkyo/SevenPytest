# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class LoginPage(BaseMiniumPage):
    """ 登录页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def login_btn(self):
            """登录"""

            selector = 'view.login>view.button>button'
            inner_text = '登录'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def form(self):
            """ 手机号码输入框和验证码输入框所在的表单"""

            selector = 'view.login>mp-form#form'
            return self.page.get_element(selector)

        @property
        def phone_number_inputbox(self):
            """手机号码输入框"""

            tips = '请输入号码'
            attrname = 'placeholder'
            self.form.click()
            self.page.sleep(2)
            mp_cells_list = self.form.get_elements('mp-cells')
            right_el_input = None
            for mp_cells in mp_cells_list:
                mp_cells.click()
                self.page.sleep(2)
                mp_cell_list = mp_cells.get_elements('mp-cell')
                for mpcell in mp_cell_list:
                    mpcell.click()
                    self.page.sleep(2)
                    el_inputs = mpcell.get_elements('view>view>input')

                    for el_input in el_inputs:
                        if "".join(el_input.attribute(attrname)) == tips:
                            right_el_input = el_input
                            break
                    if right_el_input:
                        break
                if right_el_input:
                    break
            if not right_el_input:
                self.page.raise_error('找不到手机输入框元素(attribute:{}="{}")'.format(attrname, tips))
            return right_el_input

        @property
        def checkcode_inputbox(self):
            """验证码输入框"""

            tips = '请输入验证码'
            attrname = 'placeholder'
            self.form.click()
            self.page.sleep(2)
            mp_cells_list = self.form.get_elements('mp-cells')
            right_el_input = None
            for mp_cells in mp_cells_list:
                mp_cells.click()
                self.page.sleep(2)
                mp_cell_list = mp_cells.get_elements('mp-cell')
                for mpcell in mp_cell_list:
                    mpcell.click()
                    self.page.sleep(2)
                    el_inputs = mpcell.get_elements('view>view>input')
                    for el_input in el_inputs:
                        if "".join(el_input.attribute(attrname)) == tips:
                            right_el_input = el_input
                            break
                    if right_el_input:
                        break
                if right_el_input:
                    break
            if not right_el_input:
                self.page.raise_error('找不到验证码输入框元素(attribute:{}="{}")'.format(attrname, tips))
            return right_el_input

        @property
        def checkcode_btn(self):
            """获取验证码按钮"""

            selector = '.weui-vcode-btn'
            inner_text = '获取验证码'
            self.form.click()
            self.page.sleep(2)
            mp_cells_list = self.form.get_elements('mp-cells')
            right_el_btn = None
            for mp_cells in mp_cells_list:
                mp_cells.click()
                self.page.sleep(2)
                mp_cell_list = mp_cells.get_elements('mp-cell')
                for mpcell in mp_cell_list:
                    mpcell.click()
                    self.page.sleep(5)
                    el_btns = mpcell.get_elements(selector)
                    for el_btn in el_btns:
                        if el_btn.inner_text == inner_text:
                            right_el_btn = el_btn
                            break
                    if right_el_btn:
                        break
                if right_el_btn:
                    break
            right_el_btn.outer_wxml
            return right_el_btn

        @property
        def enable_register_checkbox(self):
            """若手机号未注册，将会进入注册流程。注册即视为同意"""

            selector = 'view.login>checkbox-group>label>view'
            inner_text = '若手机号未注册，将会进入注册流程。注册即视为同意'
            el_views = self.page.get_elements(selector)
            el_icon = None
            for el_view in el_views:
                if el_view.get_element('checkbox#weuiAgree'):
                    el_icon = el_view.get_element('view')
                    break
            if not el_icon:
                self.page.raise_error('找不到[{}]复选框'.format(inner_text))
            return el_icon

    class Actions(BaseMiniumPage.Actions):
        def login(self):
            """点击登录按钮"""

            self.page.elements.login_btn.click()
            return self

        def input_phone_number(self, number):
            """输入手机号码"""

            self.page.elements.phone_number_inputbox.trigger("input", {"value": number})
            return self

        def input_checkcode(self, checkcode):
            """输入验证码"""
            el = self.page.elements.checkcode_inputbox
            # el.trigger("focus", {"value": True})
            el.click()
            self.sleep(3)
            el.trigger("input", {"value": checkcode})
            # el.trigger("bindinput", {"inner_text": checkcode})
            self.sleep(1)
            print(el.outer_wxml)
            return self

        def click_get_checkcode(self):
            """点击获取验证码按钮"""

            self.page.elements.checkcode_btn.click()
            return self

        def check_argee(self):
            """点击[若手机号未注册，将会进入注册流程。注册即视为同意]复选框"""

            self.page.elements.enable_register_checkbox.click()
            return self
