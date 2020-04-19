# -*- coding:utf-8 -*-

"""
测试断言
"""

from sevenautotest.exceptions import TestAssertException
from .typetools import (strclass,safe_repr)

__version__ = "1.0"
__author__ = "si wen wei"

def fail(message):    
    raise TestAssertException(message)

def format_msg(msg, standard_msg):
    
    if msg is None:
        return standard_msg
    try:
        return '%s : %s' % (standard_msg, msg)
    except UnicodeDecodeError:
        return  '%s : %s' % (safe_repr(standard_msg), safe_repr(msg))

def assert_is_instance(obj, cls, msg=None):    
    if not isinstance(obj, cls):
        standard_msg = '%s is not an instance of %r' % (safe_repr(obj), cls)
        fail(format_msg(msg, standard_msg))
 
def assert_equals(actual, expected, msg=None):
    if actual != expected:
        standard_msg = "%s(实际) != %s(预期)" % (actual, expected)
        fail(format_msg(msg, standard_msg))