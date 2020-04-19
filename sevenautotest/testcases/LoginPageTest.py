# -*- coding:utf-8 -*-

"""
登录页面测试示例
"""

__version__ = "1.0"
__author__ = "si wen wei"

import pytest
from sevenautotest import settings
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.login import LoginPage

class LoginPageTest(BaseTestCase):
    
    def setup_class(self):
        
        pass
        
    def setup_method(self):
        
        pass   
    
    @pytest.mark.skip(reason="跳过")
    @pytest.mark.testcase("成功登陆测试", author="siwenwei", editor="")
    def test_successfully_login(self, testdata):
        
        name    = testdata.get("用户名")
        pwd     = testdata.get("密码")
        url     = testdata.get("登录页面URL")
        
        page    = LoginPage()
        page.chrome().maximize_window().open_url(url).actions.select_login_frame().sleep(1).username(name).password(pwd).sleep(2).login().sleep(3)
        page.screenshot("successfully login.png")
        page.sleep(3)
        
    def teardown_method(self):
        
        pass
        
    def teardown_class(self):
        
        self.DRIVER_MANAGER.close_all_drivers()
        
if __name__=="__main__":
    pass