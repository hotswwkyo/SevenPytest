# -*- coding:utf-8 -*-

"""

"""

class UITestException(Exception):
    pass

class NoOpenDriver(UITestException):
    pass
    
class NoOpenBrowser(UITestException):
    pass
    
class MarkerException(UITestException):
    pass

class ConstAttributeException(MarkerException):
    pass
    
class WindowNotFound(UITestException):
    pass