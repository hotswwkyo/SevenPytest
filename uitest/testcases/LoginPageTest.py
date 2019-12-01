# -*- coding:utf-8 -*-

"""
登录页面测试示例
@author siwenwei
"""
import pytest
from uitest import settings
from uitest.testcases import AbstractTestCase
from uitest.pages.login import LoginPage

class LoginPageTest(AbstractTestCase):
    
    def setup_class(self):
        
        pass
        
    def setup_method(self):
        
        pass    
    
    @pytest.mark.testcase("成功登陆测试", author="siwenwei", editor="")
    def test_successfully_login(self, testdata):
        
        name    = testdata.get("用户名")
        pwd     = testdata.get("密码")
        url     = testdata.get("登录页面URL")
        
        page    = LoginPage()
        page.chrome(executable_path = settings.CHROME_DRIVER_PATH).maximize_window().open_url(url).actions.select_login_frame().sleep(1000).username(name).password(pwd).sleep(2000).login().sleep(3000)
        page.screenshot("successfully login.png")
        page.sleep(3000)
        
    def teardown_method(self):
        
        pass
        
    def teardown_class(self):
        
        self.BROWSER_MANAGER.close_all_browsers()
        
if __name__=="__main__":
    pass