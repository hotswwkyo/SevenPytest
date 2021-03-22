# -*- coding:utf-8 -*-
"""
Driver管理器
"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from appium import webdriver as appdriver
from sevenautotest.exceptions import NoOpenBrowser
from .DriverCache import DriverCache
from sevenautotest.utils.marker import ConstAttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager


class DriverManager(AttributeManager):

    CHROME_NAME = ConstAttributeMarker("chrome", "谷歌浏览器")
    FIREFOX_NAME = ConstAttributeMarker("firefox", "火狐浏览器")
    EDGE_NAME = ConstAttributeMarker("edge", "Edge浏览器")
    IE_NAME = ConstAttributeMarker("ie", "IE浏览器")
    OPERA_NAME = ConstAttributeMarker("opera", "欧朋（Opera）浏览器")
    SAFARI_NAME = ConstAttributeMarker("safari", "Safari浏览器")
    BLACKBERRY_NAME = ConstAttributeMarker("BlackBerry", "黑莓")
    PHANTOMJS_NAME = ConstAttributeMarker("PhantomJS", "PhantomJS 是一个无界面的webkit内核浏览器")
    ANDROID_NAME = ConstAttributeMarker("Android", "安卓")
    WEBKITGTK_NAME = ConstAttributeMarker("WebKitGTK", "WebKitGTK")

    def __init__(self, script_timeout=5.0, implicit_wait_timeout=0.0):
        """
        @param script_timeout Set the amount of time(seconds) that the script should wait before throwing an error.
        @param implicit_wait_timeout Sets a sticky timeout to implicitly wait for an element to be found, or a command to complete.This method only needs to be called one time per session
        @see selenium.webdriver.remote.webdriver.set_script_timeout
        @see selenium.webdriver.remote.webdriver.implicitly_wait
        """

        self.script_timeout = script_timeout
        self.implicit_wait_timeout = implicit_wait_timeout
        self._driver_cache = DriverCache()

    @property
    def browser(self):
        """当前的浏览器，如果没有打开的浏览器将抛出异常NoOpenBrowser"""

        if not self._driver_cache.current_driver:
            raise NoOpenBrowser('未打开任何浏览器')
        return self._driver_cache.current_driver

    @property
    def driver(self):
        """当前的浏览器，如果没有打开的浏览器将抛出异常NoOpenBrowser"""

        if not self._driver_cache.current_driver:
            raise NoOpenBrowser('未运行任何driver')
        return self._driver_cache.current_driver

    @property
    def index(self):

        return self._driver_cache.current_index

    def register_driver(self, driver, alias=None):
        """
        @param driver selenium.webdriver.remote.webdriver.WebDriver以及子类实例
        返回 WebDriver 实例在缓存中的索引
        """

        return self._driver_cache.register_driver(driver, alias)

    def close_all_drivers(self):
        self._driver_cache.close_all_drivers()

    def close_driver(self):
        """Closes the current driver."""

        if self._driver_cache.current_driver:
            self._driver_cache.close_driver()

    def close_all_browsers(self):
        """Closes all open browsers and resets the browser cache."""

        self._driver_cache.close_all_drivers()

    def close_browser(self):
        """Closes the current browser."""

        if self._driver_cache.current_driver:
            self._driver_cache.close_driver()

    def open_app(self,
                 command_executor='http://127.0.0.1:4444/wd/hub',
                 alias=None,
                 desired_capabilities=None,
                 implicit_wait_timeout=0.0,
                 browser_profile=None,
                 proxy=None,
                 keep_alive=True,
                 direct_connection=False):
        app = appdriver.Remote(command_executor=command_executor,
                               desired_capabilities=desired_capabilities,
                               browser_profile=browser_profile,
                               proxy=proxy,
                               keep_alive=keep_alive,
                               direct_connection=direct_connection)
        print('Opened application with session id %s' % app.session_id)
        try:
            app.set_script_timeout(self.script_timeout)
        except WebDriverException:
            pass
        self.implicit_wait_timeout = implicit_wait_timeout
        app.implicitly_wait(self.implicit_wait_timeout)
        return self.register_driver(app, alias)

    def open_browser(self, name, url=None, alias=None, *args, **kwargs):

        index = self._driver_cache.get_index(alias)
        if index:
            self.switch_browser(alias)
            if url:
                self.open_url(url)
            return index
        return self._open_new_browser(name, url, alias, *args, **kwargs)

    def _open_new_browser(self, name, url=None, alias=None, *args, **kwargs):

        browser = self._make_browser(name, *args, **kwargs)
        browser.set_script_timeout(self.script_timeout)
        browser.implicitly_wait(self.implicit_wait_timeout)
        index = self.register_driver(browser, alias)
        if url:
            browser.get(url)
        return index

    def ie(self, url=None, alias=None, *args, **kwargs):

        return self.open_browser(self.IE_NAME, url, alias, *args, **kwargs)

    def chrome(self, url=None, alias=None, *args, **kwargs):
        return self.open_browser(self.CHROME_NAME, url, alias, *args, **kwargs)

    def firefox(self, url=None, alias=None, *args, **kwargs):
        return self.open_browser(self.FIREFOX_NAME, url, alias, *args, **kwargs)

    def switch_browser(self, index_or_alias):
        """通过索引和别名切换浏览器"""

        try:
            self._driver_cache.switch_driver(index_or_alias)
        except RuntimeError:
            raise RuntimeError("No browser with index or alias '%s' found." % index_or_alias)
        # self.debug('Switched to browser with Selenium session id %s.'
        # % self.driver.session_id)

    def switch_driver(self, index_or_alias):
        """通过索引和别名切换驱动"""
        self.switch_browser(index_or_alias)

    def open_url(self, url):
        """打开指定的url"""

        self.browser.get(url)

    def set_browsers_script_timeout(self, time_to_wait):

        old_timeout = self.script_timeout
        self.script_timeout = time_to_wait
        for driver in self._driver_cache.active_drivers:
            driver.set_script_timeout(self.script_timeout)
        return old_timeout

    def set_active_browsers_implicit_wait(self, time_to_wait):

        old_wait = self.implicit_wait_timeout
        self.implicit_wait_timeout = time_to_wait
        for driver in self._driver_cache.active_drivers:
            driver.implicitly_wait(self.implicit_wait_timeout)
        return old_wait

    def set_browser_implicit_wait(self, time_to_wait):
        """设置浏览器隐式等待找到元素

        @param time_to_wait 等待超时时间(秒)
        @see selenium.webdriver.remote.webdriver.implicitly_wait
        """
        self.browser.implicitly_wait(time_to_wait)

    def _make_browser(self, name, *args, **kwargs):

        name = name.lower()
        if name == self.CHROME_NAME.lower():
            return webdriver.Chrome(*args, **kwargs)

        elif name == self.FIREFOX_NAME.lower():
            return webdriver.Firefox(*args, **kwargs)

        elif name == self.EDGE_NAME.lower():
            return webdriver.Edge(*args, **kwargs)

        elif name == self.IE_NAME.lower():
            return webdriver.Ie(*args, **kwargs)

        elif name == self.OPERA_NAME.lower():
            return webdriver.Opera(*args, **kwargs)

        elif name == self.SAFARI_NAME.lower():
            return webdriver.Safari(*args, **kwargs)

        elif name == self.BLACKBERRY_NAME.lower():
            return webdriver.BlackBerry(*args, **kwargs)

        elif name == self.PHANTOMJS_NAME.lower():
            return webdriver.PhantomJS(*args, **kwargs)

        elif name == self.ANDROID_NAME.lower():
            return webdriver.Android(*args, **kwargs)

        elif name == self.WEBKITGTK_NAME.lower():
            return webdriver.WebKitGTK(*args, **kwargs)

        else:
            raise ValueError('{} is not a supported browser.'.format(name))
