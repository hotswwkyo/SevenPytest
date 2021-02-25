# -*- coding:utf-8 -*-
"""

"""


class TestException(Exception):
    pass


class UITestException(TestException):
    pass


class NoOpenDriver(UITestException):
    pass


class NoOpenBrowser(UITestException):
    pass


class MarkerException(TestException):
    pass


class ConstAttributeException(MarkerException):
    pass


class WindowNotFound(UITestException):
    pass


class TestAssertException(TestException):
    pass
