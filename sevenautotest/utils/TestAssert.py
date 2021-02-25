# -*- coding:utf-8 -*-
"""
测试断言
"""

from sevenautotest.exceptions import TestAssertException
from .typetools import safe_repr

__version__ = "1.0"
__author__ = "si wen wei"


def _report_failure(msg):
    if msg is None:
        raise TestAssertException()
    raise TestAssertException(msg)


def fail(msg=None):
    """标记测试失败，抛出测试失败信息"""
    _report_failure(msg)


def format_msg(msg, standard_msg):

    if msg is None:
        return standard_msg
    try:
        return '%s : %s' % (standard_msg, msg)
    except UnicodeDecodeError:
        return '%s : %s' % (safe_repr(standard_msg), safe_repr(msg))


def assert_is_instance(obj, cls, msg=None):
    """不是类的实例则测试失败"""
    if not isinstance(obj, cls):
        s_msg = '%s is not an instance of %r' % (safe_repr(obj), cls)
        _report_failure(format_msg(msg, s_msg))


def assert_true(expr, msg=None):
    """表达式不为真则测试失败"""

    if not expr:
        s_msg = '%s is not true' % safe_repr(expr)
        _report_failure(format_msg(msg, s_msg))


def assert_false(expr, msg=None):
    """表达式不为假则测试失败"""

    if not expr:
        s_msg = '%s is not false' % safe_repr(expr)
        _report_failure(format_msg(msg, s_msg))


def assert_none(obj, msg=None):

    if obj is not None:
        s_msg = '%s is not None' % safe_repr(obj)
        _report_failure(format_msg(msg, s_msg))


def assert_not_none(obj, msg=None):

    if obj is None:
        s_msg = '%s is None' % safe_repr(obj)
        _report_failure(format_msg(msg, s_msg))


def assert_raises(exc_class, callable_obj, *args, **kwargs):

    try:
        callable_obj(*args, **kwargs)
    except exc_class as err:
        return err
    else:
        if hasattr(exc_class, '__name__'):
            exc_name = exc_class.__name__
        else:
            exc_name = safe_repr(exc_class)
        s_msg = '%s not raised' % exc_name
        _report_failure(format_msg(None, s_msg))


def assert_equal(first, second, msg=None):
    """判断是否相等"""
    if not (first == second):
        s_msg = "%s != %s" % (safe_repr(first), safe_repr(second))
        _report_failure(format_msg(msg, s_msg))


def assert_not_equal(first, second, msg=None):
    if first == second:
        s_msg = "%s != %s" % (safe_repr(first), safe_repr(second))
        _report_failure(format_msg(msg, s_msg))


def assert_almost_equal(first, second, places=7, msg=None):
    """

    Args:
        places: 精度，四舍五入保留几位小数
    """
    if round(second - first, places) != 0:
        s_msg = "%s != %s" % (safe_repr(first), safe_repr(second))
        _report_failure(format_msg(msg, s_msg))


def assert_not_almost_equal(first, second, places=7, msg=None):
    """

    Args:
        places: 精度，四舍五入保留几位小数
    """
    if round(second - first, places) == 0:
        s_msg = "%s != %s" % (safe_repr(first), safe_repr(second))
        _report_failure(format_msg(msg, s_msg))
