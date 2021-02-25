# -*- coding:utf-8 -*-
"""
登录页面示例
"""
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators


class LoginEmailPage(BasePage):
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def login_frame(self, locators):

            xpath = locators.get("login_frame")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def username(self, locators):
            """用户名输入框"""

            xpath = locators.get("用户名")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def password(self, locators):
            """密码输入框"""

            xpath = locators.get("密码")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def auto_login(self, locators):
            """下次自动登录复选框"""

            xpath = locators.get("下次自动登录")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def login(self, locators):
            """登录按钮"""

            xpath = locators.get("登录")
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def select_login_frame(self):
            """进入frame"""

            self.page.select_frame(self.page.elements.login_frame)
            return self

        def move_to_login_btn(self):

            self.page.action_chains.move_to_element(self.page.elements.login).perform()
            # self.page.action_chains.move_to_element_with_offset(self.page.elements.auto_login,0,0).perform()
            return self

        def username(self, name):
            """输入用户名"""

            self.page.elements.username.clear()
            self.page.elements.username.send_keys(name)
            return self

        def password(self, pwd):
            """输入密码"""

            self.page.elements.password.clear()
            self.page.elements.password.send_keys(pwd)
            return self

        def login(self):
            """点击登录按钮"""

            self.page.elements.login.click()
            return self
