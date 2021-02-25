# -*- coding:utf-8 -*-
import pytest
from sevenautotest import settings
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.fxjs.LoginPage import LoginPage
from sevenautotest.testobjects.pages.apppages.fxjs.HomePage import HomePage
from sevenautotest.testobjects.pages.apppages.fxjs.SettlementMainPage import SettlementMainPage


class LoginPageTest(BaseTestCase):
    """中影发行结算登录页面测试"""
    def setup_class(self):
        self.desired_caps = settings.APP_DESIRED_CAPS
        self.server_url = settings.APPIUM_SERVER
        # adb shell am start -W -n com.zgdygf.zygfpfapp/io.dcloud.PandoraEntry

    def setup_method(self):

        pass

    @pytest.mark.testcase("成功登录发行结算app测试", author="siwenwei", editor="")
    def test_successfully_login(self, testdata):

        name = testdata.get("用户名")
        pwd = testdata.get("密码")

        page = LoginPage()
        page.open_app(self.server_url, desired_capabilities=self.desired_caps, implicit_wait_timeout=10)
        page.actions.click_continue_btn().sleep(2).click_confirm_btn().sleep(2).username(name).password(pwd).login().sleep(2).reminder().sleep(21)
        # HomePage().elements.settlement_tab
        HomePage().actions.sleep(2).click_settlement_tab()
        sp = SettlementMainPage()
        sp.actions.sleep(7).swipe_to_select_year("2019年").sleep(7).input_film_name("单行道").click_search().sleep(3)
        page.hide_keyboard()
        sp.actions.click_film_item("单行道")

    def teardown_method(self):

        pass

    def teardown_class(self):

        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
