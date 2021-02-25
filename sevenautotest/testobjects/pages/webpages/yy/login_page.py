# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class LoginPage(BasePage):
    """雨燕管理后台登录页面"""
    class Elements(BasePage.Elements):
        @property
        def username_inputbox(self):
            """用户名输入框"""

            xpath = '//input[@id="username"]'
            return self.page.find_element_by_xpath(xpath)

        @property
        def password_inputbox(self):
            """密码输入框"""

            xpath = '//input[@id="password"]'
            return self.page.find_element_by_xpath(xpath)

        @property
        def vcode_inputbox(self):
            """验证码输入框"""

            xpath = '//input[@id="inputCode"]'
            return self.page.find_element_by_xpath(xpath)

        @property
        def login_btn(self):
            """确定按钮"""

            name = '确 定'
            xpath = '//form[@id="formLogin"]//button/span[normalize-space()="{name}"]/parent::button'.format(name=name)
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def input_username(self, username):
            """输入用户名"""

            self.page.elements.username_inputbox.clear()
            self.page.elements.username_inputbox.send_keys(username)
            return self

        def input_password(self, password):
            """输入密码"""

            self.page.elements.password_inputbox.clear()
            self.page.elements.password_inputbox.send_keys(password)
            return self

        def input_vcode(self, vcode):
            """输入验证码"""

            self.page.elements.vcode_inputbox.clear()
            self.page.elements.vcode_inputbox.send_keys(vcode)
            return self

        def login(self):
            """点击确定按钮"""
            self.page.elements.login_btn.click()
            return self
