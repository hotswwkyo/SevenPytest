# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

_MAX_LENGTH = 80


def is_string(value):

    return isinstance(value, (str))


def is_webelement(element):

    return isinstance(element, WebElement)


def is_webdriver(value):

    return isinstance(value, WebDriver)


def safe_repr(obj, short=False):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < _MAX_LENGTH:
        return result
    return result[:_MAX_LENGTH] + ' [truncated]...'


def strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__qualname__)
