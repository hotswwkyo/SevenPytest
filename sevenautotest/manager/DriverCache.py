# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from sevenautotest.utils import typetools
from sevenautotest.utils import StringKeyDict
from sevenautotest.exceptions import NoOpenDriver


class DriverCache(object):
    def __init__(self, no_current_driver_msg="No current Driver"):

        self._all_drivers = []
        self._current_driver = None
        self._closed_drivers = set()
        self.no_current_driver_msg = no_current_driver_msg
        self._driver_alias = StringKeyDict.StringKeyDict()

    @property
    def current_driver(self):

        if not self:
            raise NoOpenDriver(self.no_current_driver_msg)
        return self._current_driver

    @property
    def current_index(self):

        if not self:
            return None
        for index, driver in enumerate(self._all_drivers):
            if driver is self._current_driver:
                return index + 1

    def register_driver(self, driver, alias=None):
        """注册driver，并返回注册成功后，它在缓存中的位置索引(索引号从1开始)

        @param driver 浏览器驱动对象
        @param alias 字符串类型，忽略大小写和空格
        """

        self._current_driver = driver
        self._all_drivers.append(driver)
        index = len(self._all_drivers)
        if typetools.is_string(alias):
            self._driver_alias[alias] = index
        return index

    def switch_driver(self, alias_or_index):
        """通过driver 别名或索引切换到对应的driver

        @see register_driver(self, driver, alias = None)
        """
        self._current_driver = self._get_driver(alias_or_index)
        return self._current_driver

    def _get_driver(self, alias_or_index=None):
        """通过别名或索引或者缓存中浏览器驱动对象

        @param alias_or_index 如果传入None则返回当前激活的浏览器对象，否则根据指定的别名或索引查找并返回
        @see register_driver(self, driver, alias = None)
        """
        if alias_or_index is None:
            if not self:
                raise RuntimeError(self.no_current_driver_msg)
            return self._current_driver
        try:
            index = self._resolve_alias_or_index(alias_or_index)
        except ValueError:
            raise RuntimeError("Non-existing index or alias '%s'." % alias_or_index)
        return self._all_drivers[index - 1]

    @property
    def drivers(self):

        return self._all_drivers

    @property
    def active_drivers(self):

        open_drivers = []
        for driver in self._all_drivers:
            if driver not in self._closed_drivers:
                open_drivers.append(driver)
        return open_drivers

    def close_driver(self):

        if self._current_driver:
            driver = self._current_driver
            self._current_driver.quit()
            self._current_driver = None
            self._closed_drivers.add(driver)

    def close_all_drivers(self):

        for driver in self._all_drivers:
            if driver not in self._closed_drivers:
                driver.quit()
        self.clear_empty_cache()
        return self._current_driver

    def clear_empty_cache(self):

        self._all_drivers = []
        self._current_driver = None
        self._closed_drivers = set()
        self._driver_alias = StringKeyDict.StringKeyDict()

    def get_index(self, alias_or_index):

        try:
            index = self._resolve_alias_or_index(alias_or_index)
        except ValueError:
            return None
        try:
            driver = self._get_driver(alias_or_index)
        except RuntimeError:
            return None
        return None if driver in self._closed_drivers else index

    def _resolve_alias_or_index(self, alias_or_index):
        try:
            return self._resolve_alias(alias_or_index)
        except ValueError:
            return self._resolve_index(alias_or_index)

    def _resolve_alias(self, alias):
        if typetools.is_string(alias):
            try:
                return self._driver_alias[alias]
            except KeyError:
                pass
        raise ValueError

    def _resolve_index(self, index):
        try:
            index = int(index)
        except TypeError:
            raise ValueError
        if not 0 < index <= len(self._all_drivers):
            raise ValueError
        return index

    def __nonzero__(self):

        return self._current_driver is not None and isinstance(self._current_driver, RemoteWebDriver)
