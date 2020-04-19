# -*- coding:utf-8 -*-

"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from .AbstractTestCase import AbstractTestCase

class BaseTestCase(AbstractTestCase):
    
    @property
    def driver_manager(self):
        return self.__class__.DRIVER_MANAGER