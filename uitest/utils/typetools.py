# -*- coding:utf-8 -*-

"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

def is_string(value):
    
    return isinstance(value, (str))
    
def is_webelement(element):
    
    return isinstance(element, WebElement)
    
def is_webdriver(value):
    
    return isinstance(value, WebDriver)