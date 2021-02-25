# -*- coding:utf-8 -*-
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators


class LoginPage(BasePage):
    """
    中影发行结算登录页面示例
    """
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def continue_btn(self, locators):
            """授权页->继续按钮"""

            xpath = locators.get("继续")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def confirm_btn(self, locators):
            """更新提示->确定按钮"""

            xpath = locators.get("确定")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def username(self, locators):
            """用户名输入框"""

            xpath = locators.get("用户名")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def password(self, locators):
            """密码输入框"""

            xpath = locators.get("密码")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def login(self, locators):
            """登录按钮"""

            xpath = locators.get("登录")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def reminder(self, locators):
            """下次提醒"""

            xpath = locators.get("下次提醒")
            return self.page.find_element_by_android_uiautomator(xpath)

    class Actions(BasePage.Actions):
        def click_continue_btn(self):
            self.page.elements.continue_btn.click()
            return self

        def click_confirm_btn(self):
            self.page.elements.confirm_btn.click()
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

        def reminder(self):
            """下次提醒"""

            self.page.elements.reminder.click()
            return self
