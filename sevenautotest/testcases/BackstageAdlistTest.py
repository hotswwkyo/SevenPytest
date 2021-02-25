# -*- coding:utf-8 -*-
"""

"""
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.utils.sn_generator import SerialNumbersGenerator
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.yy.indexpage import IndexPage
from sevenautotest.testobjects.pages.apppages.yy.clip_page import ClipPage
from sevenautotest.testobjects.pages.apppages.yy.preview_page import PreviewPage
from sevenautotest.testobjects.pages.webpages.yy.login_page import LoginPage as WebLoginPage
from sevenautotest.testobjects.pages.webpages.yy.home_page import HomePage
from sevenautotest.testobjects.pages.webpages.yy.adlist_page import ADListPage


class BackstageAdlistTest(BaseTestCase):
    """ 管理后台广告片列表测试"""
    def setup_class(self):

        # self.WECHAT_MANAGER.init_minium()
        self.login()

    def setup_method(self):

        pass

    @classmethod
    def login(cls):

        url = settings.URLS.get("雨燕管理后台")
        username, password = settings.USERS.get("雨燕管理后台")
        login_page = WebLoginPage()
        login_page.chrome().maximize_window().open_url(url).actions.input_username(username).input_password(password).input_vcode('at').sleep(2).login().sleep(7)

    @pytest.mark.testcase('广告片列表筛选 - 广告编号输入框输入正确的广告编号查询', author="siwenwei", editor="")
    def test_search_with_right_ad_number(self, testdata):

        ad_number = testdata.get("广告编号")
        ad_name = testdata.get("广告名称")
        userid = testdata.get("用户ID")
        save_status = testdata.get("存储状态")
        home_page = HomePage()
        home_page.actions.sleep(20).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_number": ad_number,
            "ad_name": ad_name,
            "user_id": userid,
            "save_status": save_status,
        }
        al_page.actions.ad_number(ad_number).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('广告片列表筛选 - 广告编号输入框输入错误的广告编号查询', author="siwenwei", editor="")
    def test_search_with_wrong_ad_number(self, testdata):

        ad_number = testdata.get("广告编号")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        al_page.actions.ad_number(ad_number).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('广告片列表筛选 - 广告编号输入框输入广告编号的部分字段查询', author="siwenwei", editor="")
    def test_search_with_parttext_ad_number(self, testdata):

        ad_number = testdata.get("广告编号(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        al_page.actions.ad_number(ad_number).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('广告片列表筛选 - 广告编号输入框输入特殊字符查询', author="siwenwei", editor="")
    def test_search_ad_with_special_chart(self, testdata):

        ad_number = testdata.get("广告编号查询输入框")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        al_page.actions.ad_number(ad_number).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('广告片列表筛选 - 广告名称输入框输入正确的广告名称查询', author="siwenwei", editor="")
    def test_search_with_right_ad_name(self, testdata):

        s_name = testdata.get("广告名称(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.ad_name(s_name).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo, check_total=True)

    @pytest.mark.testcase('广告片列表筛选 - 广告名称输入框输入错误的广告名称查询', author="siwenwei", editor="")
    def test_search_with_wrong_ad_name(self, testdata):

        s_name = testdata.get("广告名称(查询)")
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)
        al_page = ADListPage()
        al_page.actions.ad_name(s_name).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('广告片列表筛选 - 广告名称输入框输入部分广告名称查询测试', author="siwenwei", editor="")
    def test_search_with_parttext_ad_name(self, testdata):

        s_name = testdata.get("广告名称(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.ad_name(s_name).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo).see(all_rowinfo[0]).sleep(3)

    @pytest.mark.testcase('广告片列表筛选 - 用户ID输入框输入正确的用户ID查询', author="siwenwei", editor="")
    def test_search_with_right_userid(self, testdata):

        userid = testdata.get("用户ID(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.user_id(userid).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo, check_total=True)

    @pytest.mark.testcase('广告片列表筛选 - 用户ID输入框输入错误的用户ID查询', author="siwenwei", editor="")
    def test_search_with_wrong_userid(self, testdata):

        userid = testdata.get("用户ID")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        al_page.actions.user_id(userid).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('广告片列表筛选 - 广告编号和用户ID输入框输入正确的广告编号和用户ID查询', author="siwenwei", editor="")
    def test_search_with_right_number_and_userid(self, testdata):

        ad_number = testdata.get("广告编号")
        ad_name = testdata.get("广告名称")
        userid = testdata.get("用户ID")
        save_status = testdata.get("存储状态")
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_number": ad_number,
            "ad_name": ad_name,
            "user_id": userid,
            "save_status": save_status,
        }
        al_page.actions.ad_number(ad_number).user_id(userid).sleep(1).search().sleep(3).check_adlist_table(rowinfo, check_total=True)

    @pytest.mark.testcase('广告片列表筛选 - 存储状态选择已发布查询', author="siwenwei", editor="")
    def test_search_with_release_status(self, testdata):

        s_status = testdata.get("存储状态(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                # "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.select_status(s_status).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo)

    @pytest.mark.testcase('广告片列表筛选 - 存储状态选择用户已删除查询', author="siwenwei", editor="")
    def test_search_with_user_deleted_status(self, testdata):

        s_status = testdata.get("存储状态(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.select_status(s_status).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo)

    @pytest.mark.testcase('广告片列表筛选 - 存储状态选择系统已删除查询', author="siwenwei", editor="")
    def test_search_with_system_deleted_status(self, testdata):

        s_status = testdata.get("存储状态(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.select_status(s_status).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo)

    @pytest.mark.testcase('广告片列表筛选 - 广告编号输入框、广告名称输入框和用户ID输入框输入正确，存储状态选择匹配的状态查询', author="siwenwei", editor="")
    def test_search_with_all_query_terms_is_right(self, testdata):

        s_number = testdata.get("广告编号(查询)")
        s_name = testdata.get("广告名称(查询)")
        s_userid = testdata.get("用户ID(查询)")
        s_status = testdata.get("存储状态(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(2).page.switch_current_window()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        expected_ads = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        al_page = ADListPage()
        all_rowinfo = []
        for expected_ad in expected_ads:
            all_rowinfo.append({
                "ad_number": expected_ad.get("广告编号"),
                "ad_name": expected_ad.get("广告名称"),
                "user_id": expected_ad.get("用户ID"),
                "save_status": expected_ad.get("存储状态"),
            })
        al_page.actions.ad_number(s_number).ad_name(s_name).user_id(s_userid).select_status(s_status).sleep(1).search().sleep(3).check_adlist_table(*all_rowinfo, check_total=True)

    @pytest.mark.testcase('广告片列表页 - 用户发布一个只有一张图片的广告', author="siwenwei", editor="")
    def test_search_ad_after_release_ad_that_only_one_picture(self, testdata):

        ad_name = testdata.get("广告片名称")
        ad_duration = testdata.get("视频时长")
        filepath = testdata.get("图片文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_picture_btn().sleep(2).input_upload_picture_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
            "ad_duration": ad_duration,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('广告片列表页 - 用户发布一个时长小于一分钟的N秒视频广告', author="siwenwei", editor="")
    def test_search_ad_after_release_ns_video_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
        ad_duration = testdata.get("视频时长")
        filepath = testdata.get("视频文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_video_btn().sleep(2).input_upload_video_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
            "ad_duration": ad_duration,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('广告片列表页 - 用户发布一个时长小于100秒大于一分钟的N秒视频广告', author="siwenwei", editor="")
    def test_search_ad_after_release_ns_video_ad_1(self, testdata):

        ad_name = testdata.get("广告片名称")
        ad_duration = testdata.get("视频时长")
        filepath = testdata.get("视频文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_video_btn().sleep(2).input_upload_video_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
            "ad_duration": ad_duration,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('广告片列表页 - 用户发布一个时长大于100秒的N秒视频广告', author="siwenwei", editor="")
    def test_search_ad_after_release_ns_video_ad_2(self, testdata):

        ad_name = testdata.get("广告片名称")
        ad_duration = testdata.get("视频时长")
        filepath = testdata.get("视频文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_video_btn().sleep(2).input_upload_video_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
            "ad_duration": ad_duration,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('广告片列表页 - 用户发布一个时长大于300秒的N秒视频广告', author="siwenwei", editor="")
    def test_search_ad_after_release_ns_video_ad_3(self, testdata):

        ad_name = testdata.get("广告片名称")
        ad_duration = testdata.get("视频时长")
        filepath = testdata.get("视频文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_video_btn().sleep(2).input_upload_video_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
            "ad_duration": ad_duration,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    def teardown_method(self):

        pass

    def teardown_class(self):

        # self.WECHAT_MANAGER.release_minium()
        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
