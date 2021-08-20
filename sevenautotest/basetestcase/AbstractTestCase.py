# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from sevenautotest.utils.marker import AttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager
from sevenautotest.basepage import AbstractBasePage
from sevenautotest.basepage.abstract_base_minium_page import AbstractBaseMiniumPage


class AbstractTestCase(AttributeManager):

    DRIVER_MANAGER = AttributeMarker(AbstractBasePage.DRIVER_MANAGER, True, "Driver管理器")
    WECHAT_MANAGER = AttributeMarker(AbstractBaseMiniumPage.WECHAT_MANAGER, True, "微信小程序测试库minium管理器")
    WIN_APP_DRIVER_HELPER = AttributeMarker(AbstractBasePage.WIN_APP_DRIVER_HELPER, True, "启动和关闭WinAppDriver.exe助手")
