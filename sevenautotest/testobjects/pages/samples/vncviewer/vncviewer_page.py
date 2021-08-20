#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: 思文伟
@Date: 2021/08/20
'''

from sevenautotest.basepage import BasePage


class VNCViewerPage(BasePage):
    """VNCViewer页面"""
    def init(self):
        """其实不需要这个，页面会自省的去自动创建元素和动作，这样做只是为了开发工具可以使用.引出相关的元素和动作方法"""
        cls = self.__class__
        self.elements = cls.Elements(self)
        self.actions = cls.Actions(self)

    class Elements(BasePage.Elements):
        @property
        def server_ip(self):
            """ip地址输入框"""

            return self.page.find_element_by_accessibility_id('1001')

        @property
        def ok(self):
            """ok按钮"""

            return self.page.find_element_by_name("OK")

        @property
        def pwd(self):
            """密码输入框"""

            locator = "./*"
            childrens = self.page.find_elements_by_xpath(locator)  # 获取当前窗口下的所有子元素
            element = None
            for c in childrens:
                # print("c.get_attribute("IsEnabled")=", c.get_attribute("IsEnabled"))
                if c.get_attribute("IsEnabled") == "true":  # 通过界面我们知道 只有输入密码框是可编辑的，所以使用该条件来判断是否密码输入框元素
                    element = c
                    break
            if element is None:
                message = "{} with locator '{}' not found.".format("xpath", locator)
                self.page.raise_no_such_element_exc(message)
            return element

    class Actions(BasePage.Actions):
        def server_ip(self, ip):
            """输入ip"""

            element = self.page.elements.server_ip
            element.clear()
            element.send_keys(ip)
            return self

        def ok(self):
            """点击ok按钮"""

            self.page.elements.ok.click()
            return self

        def pwd(self, password):

            element = self.page.elements.pwd
            element.clear()
            element.send_keys(password)
            return self
