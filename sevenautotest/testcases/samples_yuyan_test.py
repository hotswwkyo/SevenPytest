# -*- coding:utf-8 -*-
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.yy.indexpage import IndexPage
from sevenautotest.testobjects.pages.apppages.yy.cinema_list_page import CinemaListPage
from sevenautotest.testobjects.pages.apppages.yy.my_adlist_page import MyAdListPage


class YuyanTest(BaseTestCase):
    """雨燕测试"""
    def setup_class(self):

        self.WECHAT_MANAGER.init_minium()

    def setup_method(self):
        pass

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>去上传广告片', author="siwenwei", editor="")
    def test_jump_page_of_click_upload_ad(self, testdata):

        fn_name = helper.get_caller_name()
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1).click_cinema_ad_btn()
        clpage = CinemaListPage()
        clpage.actions.sleep(1).screenshot('{}_影院列表_'.format(fn_name)).is_page_self(settings.URLS['影院列表']).upload_ad().sleep(2)
        p = MyAdListPage()
        p.actions.screenshot('{}_我的广告素材_'.format(fn_name)).is_page_self()

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>广告片显示>更换广告片', author="siwenwei", editor="")
    def test_change_ad_to_another_in_cinemalist(self, testdata):

        oad_name = testdata.get('广告名(原)')
        nad_name = testdata.get('广告名(新)')
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1).click_cinema_ad_btn()
        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表']).upload_ad().sleep(2)
        p = MyAdListPage()
        p.actions.is_page_self().click_ad_checkbox(oad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.change().sleep(1)
        p.actions.click_ad_checkbox(nad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.find_ad_name(nad_name)

    def teardown_method(self):
        pass

    def teardown_class(self):

        self.WECHAT_MANAGER.release_minium()


if __name__ == "__main__":
    pass
