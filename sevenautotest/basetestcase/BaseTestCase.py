# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

import time
from .AbstractTestCase import AbstractTestCase
from sevenautotest.utils import TestAssert


class BaseTestCase(AbstractTestCase):
    @property
    def driver_manager(self):
        return self.__class__.DRIVER_MANAGER

    @property
    def wechat_manager(self):
        return self.__class__.WECHAT_MANAGER

    def fail(self, message=""):
        TestAssert.fail(message)

    def sleep(self, seconds):

        time.sleep(seconds)
