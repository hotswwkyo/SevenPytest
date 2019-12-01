# -*- coding:utf-8 -*-

"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from uitest.utils.marker import AttributeMarker
from uitest.utils.marker import ConstAttributeMarker
from uitest.utils.AttributeManager import AttributeManager
from uitest.pages import AbstractBasePage

class AbstractTestCase(AttributeManager):
	
	BROWSER_MANAGER = AttributeMarker(AbstractBasePage.BROWSER_MANAGER, True, "浏览器管理器")