# -*- coding:utf-8 -*-

import time
from sevenautotest.manager import minium_manager
from sevenautotest.utils.marker import AttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager


class AbstractBaseMiniumPage(AttributeManager):
    """微信小程序抽象根页面"""

    WECHAT_MANAGER = AttributeMarker(minium_manager.WECHAT_MANAGER, True, "微信小程序测试库minium管理器")

    def __init__(self, url=None):

        self.mini = self.__class__.WECHAT_MANAGER.mini
        self.native = self.__class__.WECHAT_MANAGER.native
        self.app = self.mini.app
        self.url = url

        if self.url and isinstance(self.url, str) and self.url.strip() != "":
            self.app.redirect_to(self.url)
        self._build_elements()
        self._build_actions()
        self.init()

    @property
    def current_page(self):

        return self.app.get_current_page()

    @property
    def wechat_manager(self):
        return self.__class__.WECHAT_MANAGER

    def get_element(self, selector, inner_text=None, text_contains=None, value=None, max_timeout=20):

        return self.app.get_current_page().get_element(selector, inner_text=inner_text, text_contains=text_contains, value=value, max_timeout=max_timeout)

    def get_elements(self, selector, max_timeout=20):

        return self.app.get_current_page().get_elements(selector, max_timeout=max_timeout)

    def init(self):

        pass

    def _build_elements(self):

        self.elements = self.__class__.Elements(self)

    def _build_actions(self):

        self.actions = self.__class__.Actions(self)

    def screenshot(self, name=None):

        return self.wechat_manager.screenshot(name)

    def sleep(self, seconds):
        """seconds the length of time to sleep in seconds"""
        time.sleep(seconds)
        return self

    def raise_error(self, message=''):

        raise AssertionError(message)

    class Elements(object):
        def __init__(self, page):

            self.page = page

        def sleep(self, seconds):

            self.page.sleep(seconds)
            return self

    class Actions(object):
        def __init__(self, page):

            self.page = page

        def sleep(self, seconds):

            self.page.sleep(seconds)
            return self

        def turn_to_page(self, page_number):
            """翻页， 由具体页面实现"""

            raise NotImplementedError

        def screenshot(self, name=None):

            self.page.screenshot(name)
            return self
