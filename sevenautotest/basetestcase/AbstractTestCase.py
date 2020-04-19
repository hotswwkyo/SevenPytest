# -*- coding:utf-8 -*-

"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from sevenautotest.utils.marker import AttributeMarker
from sevenautotest.utils.marker import ConstAttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager
from sevenautotest.basepage import AbstractBasePage

class AbstractTestCase(AttributeManager):
    
    DRIVER_MANAGER = AttributeMarker(AbstractBasePage.DRIVER_MANAGER, True, "Driver管理器")