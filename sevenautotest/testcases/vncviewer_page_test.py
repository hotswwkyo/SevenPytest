#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: 思文伟
@Date: 2021/08/06 15:20:32
'''

import pytest
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.samples.vncviewer.vncviewer_page import VNCViewerPage


class VNCViewerPageTest(BaseTestCase):
    """使用WinAppDriver.exe测试Window应用程序VNCViewer示例"""
    def setup_class(self):

        self.WIN_APP_DRIVER_HELPER.startup_winappdriver(r"E:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe")

    def setup_method(self):

        pass

    @pytest.mark.testcase('使用正确密码连接远程电脑桌面', author="siwenwei", editor="")
    def connect_remote_pc_desktop(self, testdata):

        ip = testdata.get("远程桌面登录账户")
        pwd = testdata.get("远程桌面登录密码")
        vnc_title = "VNC Viewer : Authentication [No Encryption]"
        desired_capabilities = {}
        desired_capabilities["app"] = r"C:\Users\cfgdc-pc 98\Desktop\vnc-4_1_2-x86_win32_viewer.exe"  # vnc viewer 的执行路径
        server_url = "http://127.0.0.1:4723"
        page = VNCViewerPage()
        page.open_window_app(server_url, desired_capabilities)

        page.actions.sleep(5).server_ip(ip).sleep(1).ok()
        # 上面点击ok后，到下一个界面显示出来需要时间，所以这里设置延时等待
        page.switch_window_by_title(vnc_title, timeout=20).actions.pwd(pwd).sleep(2).ok()

    def teardown_method(self):

        self.sleep(1)

    def teardown_class(self):

        self.DRIVER_MANAGER.close_all_drivers()
        self.WIN_APP_DRIVER_HELPER.shutdown_winappdriver()
