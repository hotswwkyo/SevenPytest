# -*- coding:utf-8 -*-
"""

"""
import datetime
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.utils import TimeTools as timetools
from sevenautotest.utils.sn_generator import SerialNumbersGenerator
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.yy.indexpage import IndexPage
from sevenautotest.testobjects.pages.apppages.yy.areapage import AreaPage
from sevenautotest.testobjects.pages.apppages.yy.calendar_page import CalendarPage
from sevenautotest.testobjects.pages.apppages.yy.ad_basket_page import ADBasketPage
from sevenautotest.testobjects.pages.apppages.yy.myself_page import MyselfPage
from sevenautotest.testobjects.pages.apppages.yy.clip_page import ClipPage
from sevenautotest.testobjects.pages.apppages.yy.preview_page import PreviewPage
from sevenautotest.testobjects.pages.apppages.yy.cinema_list_page import CinemaListPage
from sevenautotest.testobjects.pages.apppages.yy.cinema_detail_page import CinemaDetailPage
from sevenautotest.testobjects.pages.apppages.yy.my_adlist_page import MyAdListPage
from sevenautotest.testobjects.pages.apppages.yy.userinfo_page import UserInfoPage
from sevenautotest.testobjects.pages.apppages.yy.confirm_order_page import ConfirmOrderPage

from sevenautotest.testobjects.pages.webpages.yy.login_page import LoginPage as WebLoginPage
from sevenautotest.testobjects.pages.webpages.yy.home_page import HomePage
from sevenautotest.testobjects.pages.webpages.yy.adlist_page import ADListPage


class YuyanTest(BaseTestCase):
    """ 雨燕 测试 """
    def setup_class(self):

        self.WECHAT_MANAGER.init_minium()

    def setup_method(self):

        pass

    @classmethod
    def login(cls):

        url = settings.URLS.get("雨燕管理后台")
        username, password = settings.USERS.get("雨燕管理后台")
        login_page = WebLoginPage()
        login_page.chrome().maximize_window().open_url(url).actions.input_username(username).input_password(password).input_vcode('at').sleep(2).login().sleep(7)

    @pytest.mark.testcase('首页->投放地区 验证投放地区显示的正确性', author="siwenwei", editor="")
    def test_area_is_right_when_select_one_area(self, testdata):

        e_area = testdata.get("预期显示的投放地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage()
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        apage.actions.clear().sleep(1)
        for e_areainfo in e_areainfo_list:
            city = e_areainfo.get("城市")
            area = e_areainfo.get("地区")
            apage.actions.click_city(city).sleep(2).click_area(area).sleep(2)
        apage.actions.confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('首页->投放地区 验证投放地区显示的正确性', author="siwenwei", editor="")
    def test_area_is_right_when_select_more_area(self, testdata):

        self.test_area_is_right_when_select_one_area(testdata)

    @pytest.mark.testcase('首页->投放周期 不跨月份，不跨年份，验证投放周期默认显示的正确性', author="siwenwei", editor="")
    def test_defaulttime_is_right_in_indexpage(self, testdata):

        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.find_curr_duration(timetools.format_dayrange(day_diff=6))

    @pytest.mark.testcase('首页>制作广告片 已登录，首页点击制作广告按钮', author="siwenwei", editor="")
    def test_option_button_is_right_after_click_makead(self, testdata):

        ipage = IndexPage(settings.URLS['首页'])
        fn_name = helper.get_caller_name()
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        p = ipage.elements.select_upload_picture_btn
        v = ipage.elements.select_upload_video_btn
        c = ipage.elements.cancel_btn
        failmsg = []
        if not p:
            failmsg.append('选择图片 按钮不存在')
        if not v:
            failmsg.append('选择视频 按钮不存在')
        if not c:
            failmsg.append('取消 按钮不存在')
        if failmsg:
            self.fail(';'.join(failmsg))

    @pytest.mark.testcase('投放地区->地区选择->搜索结果选择的正确性', ' ', '选择一个城市的多个地区，选择成功', author="siwenwei", editor="")
    def test_successfully_choose_more_areas_of_a_city(self, testdata):

        e_area = testdata.get("预期显示的投放地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        # apage.actions.clear().sleep(1)
        for e_areainfo in e_areainfo_list:
            city = e_areainfo.get("城市")
            area = e_areainfo.get("地区")
            apage.actions.click_city(city).sleep(2).click_area(area).sleep(2)
        apage.actions.confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('投放地区->地区选择->搜索结果选择的正确性', ' ', '选择一个城市的全部地区，选择成功', author="siwenwei", editor="")
    def test_click_selectall_btn_to_select_all_areas_of_a_city(self, testdata):

        city = testdata.get("城市")
        e_area = testdata.get("预期显示的投放地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        # apage.actions.clear().sleep(1)
        apage.actions.click_city(city).sleep(2).select_all().sleep(2)
        areas = []
        for e_areainfo in e_areainfo_list:
            area = e_areainfo.get("地区")
            areas.append(area)
        apage.actions.check_area_is_selected(areas).sleep(2).confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('投放地区->地区选择->搜索结果选择的正确性', ' ', '选择多个城市的多个地区进，选择成功', author="siwenwei", editor="")
    def test_successfully_choose_more_areas_of_more_city(self, testdata):

        e_area = testdata.get("预期显示的投放地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        # apage.actions.clear().sleep(1)

        areas = []
        for e_areainfo in e_areainfo_list:
            city = e_areainfo.get("城市")
            area = e_areainfo.get("地区")
            areas.append(area)
            apage.actions.click_city(city).sleep(1).click_area(area).sleep(1)
        apage.actions.check_area_is_selected(areas).sleep(2).confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('投放地区->地区选择->搜索结果选择的正确性', ' ', '验证选择一省的一个城市的一个区', author="siwenwei", editor="")
    def test_successfully_choose_one_areas_of_one_city(self, testdata):

        e_area = testdata.get("预期显示的投放地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        # apage.actions.clear().sleep(1)
        for e_areainfo in e_areainfo_list:
            city = e_areainfo.get("城市")
            area = e_areainfo.get("地区")
            apage.actions.click_city(city).sleep(2).click_area(area).sleep(2)
        apage.actions.confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('投放地区->地区选择->清空选中城市功能', '-', '取消选中被选中地区中的一个正确性', author="siwenwei", editor="")
    def test_successfull_cancel_one_of_more_selected_areas(self, testdata):

        e_area = testdata.get("预期显示的投放地区")
        del_area = testdata.get("取消已选中的地区")
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_area()
        apage = AreaPage()
        e_areainfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        # apage.actions.clear().sleep(1)
        selected_areas = []
        for e_areainfo in e_areainfo_list:
            city = e_areainfo.get("城市")
            area = e_areainfo.get("地区")
            apage.actions.click_city(city).sleep(2).click_area(area).sleep(2)
            selected_areas.append(area)
        apage.actions.remove_selected_area(del_area)
        selected_areas.remove(del_area)
        apage.actions.sleep(3).check_area_is_selected(selected_areas).sleep(2).confirm().sleep(3)
        ipage.actions.find_curr_area(e_area)

    @pytest.mark.testcase('投放周期界面>周期选择的正确性', '-', '选择一天，点击完成，选择成功', author="siwenwei", editor="")
    def test_only_select_one_day(self, testdata):

        day_delta = testdata.get("时间间隔(以当天开始，0则当天，1则第二天)")
        # e_time = testdata.get("预期显示的投放周期")

        target = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
        year = '{}年'.format(target.year)
        month = '{}月'.format(target.month)
        day = '{}'.format(target.day)

        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date('20年', timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day).click_selected_date_btn().sleep(3)
        cpage.actions.check_selected_is_exists([target.strftime('%y年'), [target.strftime('%m/%d')]])
        cpage.actions.check_selected_total_days(1).finish().sleep(3)
        ipage.actions.find_curr_duration(target.strftime('%m月%d日'))

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择的正确性', '-', '选择连续的多天，点击完成，选择成功', author="siwenwei", editor="")
    def test_select_consecutive_days(self, testdata):

        day_delta = testdata.get("时间间隔(以当天开始，0则当天，1则第二天)")
        total = testdata.get("连续天数")

        start_day = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
        next_day = start_day
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date('20年', timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        for i in range(int(total) + 1):
            year = '{}年'.format(next_day.year)
            month = '{}月'.format(next_day.month)
            day = '{}'.format(next_day.day)
            cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
            next_day = next_day + datetime.timedelta(days=1)
        end_day = next_day
        checkdays = [start_day.strftime('%y年'), ['{} - {}'.format(start_day.strftime('%m/%d'), end_day.strftime('%m/%d'))]]
        cpage.actions.click_selected_date_btn().sleep(3).check_selected_is_exists(checkdays).check_selected_total_days(total).finish().sleep(3)
        ipage.actions.find_curr_duration('{} - {}'.format(start_day.strftime('%m月%d日'), end_day.strftime('%m月%d日')))

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择的正确性', '-', '选择(一个月内)不连续的多天，点击完成，选择成功', author="siwenwei", editor="")
    def test_select_discontinuous_days_of_month(self, testdata):

        day_delta = testdata.get("时间间隔(以当天开始，0则当天，1则第二天)")
        total = testdata.get("不连续天数")
        e_time = testdata.get("预期显示的投放周期")

        now = datetime.datetime.now()
        next_day = now + datetime.timedelta(days=int(day_delta))
        dd_list = []

        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(now.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        for i in range(int(total) + 1):
            year = '{}年'.format(next_day.year)
            month = '{}月'.format(next_day.month)
            day = '{}'.format(next_day.day)
            cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
            dd_list.append(next_day)
            next_day = next_day + datetime.timedelta(days=2)

        cpage.actions.click_selected_date_btn().sleep(3)
        day_str_list = []
        for thisday in dd_list:
            day_str_list.append(thisday.strftime('%m/%d'))
        cpage.actions.check_selected_is_exists([dd_list[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_total_days(total).finish().sleep(3)
        ipage.actions.find_curr_duration(e_time)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择的正确性', '-', '选择(一年内多个月内)不连续的多天，点击完成，选择成功', author="siwenwei", editor="")
    def test_select_discontinuous_days_of_more_month_in_one_year(self, testdata):

        total = testdata.get("每个月不连续天数")
        e_time = testdata.get("预期显示的投放周期")

        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        first_month = datetime.datetime(next_year, 1, 1)
        second_month = datetime.datetime(next_year, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)

        for next_day in [first_month, second_month]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=2)

        cpage.actions.click_selected_date_btn().sleep(3)
        day_str_list = []
        for thisday in dd_list:
            day_str_list.append(thisday.strftime('%m/%d'))
        cpage.actions.check_selected_is_exists([dd_list[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_total_days(total).finish().sleep(3)
        ipage.actions.find_curr_duration(e_time)

    def group_by_year(self, datetime_obj_list):

        only_years = []
        groups = []
        for dto in datetime_obj_list:
            if dto.year not in only_years:
                only_years.append(dto.year)
        for y in only_years:
            md_of_y = []
            for one in datetime_obj_list:
                if y == one.year:
                    md_of_y.append(one)
            if md_of_y:
                groups.append(md_of_y)
        return groups

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择的正确性', '-', '选择(两年内多个月内)不连续的多天，点击完成，选择成功', author="siwenwei", editor="")
    def test_select_discontinuous_days_of_more_month_in_two_year(self, testdata):

        total = testdata.get("每个月不连续天数")
        e_time = testdata.get("预期显示的投放周期")

        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        month_1 = datetime.datetime(next_year, 1, 1)
        month_2 = datetime.datetime(next_year, 2, 1)
        month_3 = datetime.datetime(next_year + 1, 1, 1)
        month_4 = datetime.datetime(next_year + 1, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)

        for next_day in [month_1, month_2, month_3, month_4]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=2)
        cpage.actions.click_selected_date_btn().sleep(3)
        checkdaylist = []
        for group in self.group_by_year(dd_list):
            day_str_list = []
            for thisday in group:
                day_str_list.append(thisday.strftime('%m/%d'))
            checkdaylist.append([group[0].strftime('%y年'), day_str_list])

        cpage.actions.check_selected_is_exists(*checkdaylist)
        cpage.actions.check_selected_total_days(total * 4).finish().sleep(3)
        ipage.actions.find_curr_duration(e_time)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传MP4格式的视频上传', author="siwenwei", editor="")
    def test_upload_mp4_video_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
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

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传MOV格式的视频上传', author="siwenwei", editor="")
    def test_upload_mov_video_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
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

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传MPG格式的视频上传', author="siwenwei", editor="")
    def test_upload_mpg_video_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
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

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传JPG格式的图片上传', author="siwenwei", editor="")
    def test_upload_jpg_image_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
        filepath = testdata.get("图片文件路径")
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

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传PNG格式的图片上传', author="siwenwei", editor="")
    def test_upload_png_image_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
        filepath = testdata.get("图片文件路径")
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

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('首页>制作广告片 制作广告片>上传GIF格式的图片上传', author="siwenwei", editor="")
    def test_upload_gif_image_to_make_ad(self, testdata):

        ad_name = testdata.get("广告片名称")
        filepath = testdata.get("图片文件路径")
        auto_create_name = testdata.get("是否自动生成广告片名称(Y|N)", "N")
        fn_name = helper.get_caller_name()
        if auto_create_name.upper() == 'Y'.upper():
            ad_name = settings.AD_NAME_PREFIX + SerialNumbersGenerator().serial_numbers
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).screenshot('{}_选项页面_'.format(fn_name))
        ipage.actions.click_select_upload_video_btn().sleep(2).input_upload_picture_path(filepath).sleep(3)  # 需要等待回到剪切界面

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('{}_预览界面_'.format(fn_name)).sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(10)

        self.login()
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).adlist().sleep(2)

        al_page = ADListPage()
        rowinfo = {
            "ad_name": ad_name,
        }
        al_page.actions.ad_name(ad_name).sleep(1).search().sleep(3).check_adlist_table(rowinfo)

    @pytest.mark.testcase('投放周期界面>周期选择>展开已选日期的正确性 - 选择一天，点击展开已选日期的上拉三角按钮，已选的信息显示正确', author="siwenwei", editor="")
    def test_show_selected_days_is_right_after_select_one_day(self, testdata):

        day_delta = testdata.get("时间间隔(以当天开始，0则当天，1则第二天)")
        target = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
        year = '{}年'.format(target.year)
        month = '{}月'.format(target.month)
        day = '{}'.format(target.day)

        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date('20年', timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day).click_selected_date_btn().sleep(3)
        cpage.actions.check_selected_is_exists([target.strftime('%y年'), [target.strftime('%m/%d')]])
        cpage.actions.check_selected_total_days(1)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择>展开已选日期的正确性 - 选择某个月的连续多天，点击展开已选日期的上拉三角按钮，已选的信息显示正确', author="siwenwei", editor="")
    def test_show_selected_days_is_right_after_select_consecutive_days(self, testdata):

        total = testdata.get("连续天数")

        nyear, nmonth = timetools.get_next_month_and_itself_year(datetime.datetime.now())
        start_day = datetime.datetime(nyear, nmonth, 1)
        next_day = start_day
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date('20年', timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        for i in range(int(total) + 1):
            year = '{}年'.format(next_day.year)
            month = '{}月'.format(next_day.month)
            day = '{}'.format(next_day.day)
            cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
            next_day = next_day + datetime.timedelta(days=1)
        end_day = next_day
        checkdays = [start_day.strftime('%y年'), ['{} - {}'.format(start_day.strftime('%m/%d'), end_day.strftime('%m/%d'))]]
        cpage.actions.click_selected_date_btn().sleep(3).check_selected_is_exists(checkdays).check_selected_total_days(total).sleep(3)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择>展开已选日期的正确性 - 选择一年中某几个月的连续多天，点击展开已选日期的上拉三角按钮，已选的信息显示正确', author="siwenwei", editor="")
    def test_show_is_right_after_select_discontinuous_days_of_more_month(self, testdata):

        total = testdata.get("每个月连续天数")

        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        first_month = datetime.datetime(next_year, 1, 1)
        second_month = datetime.datetime(next_year, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)

        for next_day in [first_month, second_month]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=1)

        cpage.actions.click_selected_date_btn().sleep(3)
        day_str_list = []
        for thisday in dd_list:
            day_str_list.append(thisday.strftime('%m/%d'))
        cpage.actions.check_selected_is_exists([dd_list[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_total_days(total).sleep(3)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择的正确性 - 选择一年中某几个月的不连续多天，点击展开已选日期的上拉三角按钮，已选的信息显示正确', author="siwenwei", editor="")
    def test_show_is_right_select_discontinuous_days_of_more_month_in_one_year(self, testdata):

        total = testdata.get("每个月不连续天数")

        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        first_month = datetime.datetime(next_year, 1, 1)
        second_month = datetime.datetime(next_year, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)

        for next_day in [first_month, second_month]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=2)

        cpage.actions.click_selected_date_btn().sleep(3)
        day_str_list = []
        for thisday in dd_list:
            day_str_list.append(thisday.strftime('%m/%d'))
        cpage.actions.check_selected_is_exists([dd_list[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_total_days(total)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择>展开已选日期的正确性', '-', '选择多年中某几个月的不连续多天，点击展开已选日期的上拉三角按钮，已选的信息显示正确', author="siwenwei", editor="")
    def test_show_is_right_select_discontinuous_days_of_more_month_in_two_year(self, testdata):

        total = testdata.get("每个月不连续天数")
        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        month_1 = datetime.datetime(next_year, 1, 1)
        month_2 = datetime.datetime(next_year, 2, 1)
        month_3 = datetime.datetime(next_year + 1, 1, 1)
        month_4 = datetime.datetime(next_year + 1, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        for next_day in [month_1, month_2, month_3, month_4]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=2)
        cpage.actions.click_selected_date_btn().sleep(3)
        checkdaylist = []
        for group in self.group_by_year(dd_list):
            day_str_list = []
            for thisday in group:
                day_str_list.append(thisday.strftime('%m/%d'))
            checkdaylist.append([group[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_is_exists(*checkdaylist)
        cpage.actions.check_selected_total_days(total * 4)

    # todo debug
    @pytest.mark.testcase('投放周期界面>周期选择>展开已选日期的正确性>删除已选日期的按钮的正确性 - 点击删除已选日期的按钮，界面显示正确', author="siwenwei", editor="")
    def test_remove_selected_date_by_delete_btn(self, testdata):

        total = testdata.get("每个月不连续天数")
        thistime = datetime.datetime.now()
        next_year = thistime.year + 1
        month_1 = datetime.datetime(next_year, 1, 1)
        month_2 = datetime.datetime(next_year, 2, 1)
        month_3 = datetime.datetime(next_year + 1, 1, 1)
        month_4 = datetime.datetime(next_year + 1, 2, 1)
        dd_list = []
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date(thistime.strftime('%y年'), timetools.format_dayrange(day_diff=6, start_fmt="%m/%d", end_fmt="%m/%d", sep=" - ")).sleep(1)
        for next_day in [month_1, month_2, month_3, month_4]:
            for i in range(int(total)):
                year = '{}年'.format(next_day.year)
                month = '{}月'.format(next_day.month)
                day = '{}'.format(next_day.day)
                cpage.actions.select_year(year).select_month(month).sleep(1).select_date(day)
                dd_list.append(next_day)
                next_day = next_day + datetime.timedelta(days=2)
        cpage.actions.click_selected_date_btn().sleep(3)
        checkdaylist = []
        for group in self.group_by_year(dd_list):
            day_str_list = []
            for thisday in group:
                day_str_list.append(thisday.strftime('%m/%d'))
            checkdaylist.append([group[0].strftime('%y年'), day_str_list])
        cpage.actions.check_selected_is_exists(*checkdaylist)
        cpage.actions.check_selected_total_days(total * 4)

        # todo debug
        del_date = checkdaylist[0]
        new_checkdaylist = checkdaylist[1:]
        cpage.actions.cancel_selected_date(del_date[0], del_date[1])
        cpage.actions.check_selected_is_exists(*new_checkdaylist)
        cpage.actions.check_selected_total_days(len(new_checkdaylist))

    @pytest.mark.testcase('广告制作>剪辑>预览页面按钮检测 - 预览>发布按钮检测', author="siwenwei", editor="")
    def test_check_release_function_is_right(self, testdata):

        ad_name = testdata.get("广告片名称")
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
        ppage.actions.input_title(ad_name).release().sleep(3).screenshot('{}_发布界面_'.format(fn_name)).sleep(3).confirm().sleep(3)

        clpage = CinemaListPage()
        clpage.actions.is_page_self()

        p = MyAdListPage(settings.URLS['我的广告素材'])
        p.actions.screenshot('{}_我的广告素材_'.format(fn_name)).click_ad_checkbox(ad_name)

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>去上传广告片', author="siwenwei", editor="")
    def test_jump_page_of_click_upload_ad(self, testdata):

        fn_name = helper.get_caller_name()
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).screenshot('{}_影院列表_'.format(fn_name)).is_page_self(settings.URLS['影院列表'])
        clpage.actions.upload_ad().sleep(2)

        p = MyAdListPage()
        p.actions.screenshot('{}_我的广告素材_'.format(fn_name)).is_page_self()

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>广告片显示>更换广告片', author="siwenwei", editor="")
    def test_change_ad_to_another_in_cinemalist(self, testdata):

        oad_name = testdata.get('广告名(原)')
        nad_name = testdata.get('广告名(新)')
        # fn_name = helper.get_caller_name()
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表'])
        clpage.actions.upload_ad().sleep(2)

        p = MyAdListPage()
        p.actions.is_page_self().click_ad_checkbox(oad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.change().sleep(1)
        p.actions.click_ad_checkbox(nad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.find_ad_name(nad_name)

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>加入广告栏', author="siwenwei", editor="")
    def test_add_ad_to_ad_basket_in_cinemalist(self, testdata):

        ad_name = testdata.get('广告名')
        cinema = testdata.get('影院名称')
        film = testdata.get('影片名称')
        hall = testdata.get('影厅名称')
        showdate = testdata.get('放映日期')
        showtime = testdata.get('放映时间')
        showdate_fmt = testdata.get('放映日期格式', '%Y-%m-%d')

        month_day = datetime.datetime.strptime(showdate, showdate_fmt).strftime('%m-%d')
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表'])
        clpage.actions.upload_ad().sleep(2)

        p = MyAdListPage()
        p.actions.is_page_self().click_ad_checkbox(ad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.click_cinema_item(cinema).sleep(1)

        cdp = CinemaDetailPage()
        cdp.actions.click_film(film).select_day(month_day).sleep(1).click_schedule(film, hall, showtime).sleep(1).confirm().sleep(2)
        clpage.actions.join_to_ad_basket().sleep(1).shopping_basket().sleep(1)

        bp = ADBasketPage()
        bp.actions.click_schedule_checkbox(cinema, film, hall, showdate, showtime)

    @pytest.mark.testcase('广告篮->合计价格的正确性 - 全选所有的广告篮记录，验证合计价格的正确性', author="siwenwei", editor="")
    def test_settlement_price_is_correct_with_all_schedules(self, testdata):

        ad_name = testdata.get('广告名')
        cinema = testdata.get('影院名称')
        org_price = testdata.get('原价结算')
        pt_price = testdata.get('拼团结算')
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表'])
        try:
            clpage.actions.upload_ad().sleep(2)
            p = MyAdListPage()
            p.actions.is_page_self().click_ad_checkbox(ad_name).sleep(1).to_launch().sleep(2)
        except Exception as e:
            print(str(e))
        clpage.actions.click_cinema_item(cinema).sleep(1)
        schedules = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        cdp = CinemaDetailPage()
        for schedule in schedules:
            film = schedule.get('影片名称')
            hall = schedule.get('影厅名称')
            day_delta = schedule.get('放映日期时间间隔(以当天开始，0则当天，1则第二天)')
            showdate = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
            showtime = schedule.get('放映时间')
            month_day = showdate.strftime('%m-%d')
            cdp.actions.click_film(film).select_day(month_day).sleep(1).click_schedule(film, hall, showtime).sleep(1)
        cdp.actions.confirm().sleep(2)
        clpage.actions.join_to_ad_basket().sleep(1).shopping_basket().sleep(1)
        bp = ADBasketPage()
        bp.actions.select_all().sleep(2).org_price_equals(org_price).pt_price_equals(pt_price)

    @pytest.mark.testcase('广告篮->合计价格的正确性 - 单独选中几条广告篮记录，验证合计价格的正确性', author="siwenwei", editor="")
    def test_settlement_price_is_correct_with_more_than_one_schedules(self, testdata):

        ad_name = testdata.get('广告名')
        cinema = testdata.get('影院名称')
        org_price = testdata.get('原价结算')
        pt_price = testdata.get('拼团结算')
        showdate_fmt = testdata.get('放映日期格式', '%Y-%m-%d')
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表'])
        try:
            clpage.actions.upload_ad().sleep(2)
            p = MyAdListPage()
            p.actions.is_page_self().click_ad_checkbox(ad_name).sleep(1).to_launch().sleep(2)
        except Exception as e:
            print(str(e))
        clpage.actions.click_cinema_item(cinema).sleep(1)
        schedules = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        cdp = CinemaDetailPage()
        selected_schedules = []
        for schedule in schedules:
            film = schedule.get('影片名称')
            hall = schedule.get('影厅名称')
            day_delta = schedule.get('放映日期时间间隔(以当天开始，0则当天，1则第二天)')
            showdate = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
            showtime = schedule.get('放映时间')
            month_day = showdate.strftime('%m-%d')
            selected_schedules.append((film, hall, showdate.strftime(showdate_fmt), showtime))
            cdp.actions.click_film(film).select_day(month_day).sleep(1).click_schedule(film, hall, showtime).sleep(1)
        cdp.actions.confirm().sleep(2)
        clpage.actions.join_to_ad_basket().sleep(1).shopping_basket().sleep(1)
        bp = ADBasketPage()
        for film, hall, showdate, showtime in selected_schedules:
            bp.actions.click_schedule_checkbox(cinema, film, hall, showdate, showtime)
        bp.actions.sleep(2).org_price_equals(org_price).pt_price_equals(pt_price)

    # todo(siwenwei): 广告篮页面不能正常显示，待修复后调试
    @pytest.mark.testcase('我的订单->待付款订单的正确性 - 增加待付款订单，验证待付款订单显示正确，新增的待付款订单显示在待付款订单界面', author="siwenwei", editor="")
    def test_order_to_be_paid_is_displayed_correctly(self, testdata):

        ad_name = testdata.get('广告名')
        cinema = testdata.get('影院名称')
        showdate_fmt = testdata.get('放映日期格式', '%Y-%m-%d')
        suffix_regex = r"\(\d+\)$"
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1)
        ipage.actions.click_cinema_ad_btn()

        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表'])
        try:
            clpage.actions.upload_ad().sleep(2)
            p = MyAdListPage()
            p.actions.is_page_self().click_ad_checkbox(ad_name).sleep(1).to_launch().sleep(2)
        except Exception as e:
            print(str(e))
        clpage.actions.click_cinema_item(cinema).sleep(1)
        schedules = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        cdp = CinemaDetailPage()
        selected_schedules = []
        for schedule in schedules:
            film = schedule.get('影片名称')
            hall = schedule.get('影厅名称')
            day_delta = schedule.get('放映日期时间间隔(以当天开始，0则当天，1则第二天)')
            showdate = datetime.datetime.now() + datetime.timedelta(days=int(day_delta))
            showtime = schedule.get('放映时间')
            month_day = showdate.strftime('%m-%d')
            selected_schedules.append((film, hall, showdate.strftime(showdate_fmt), showtime))
            cdp.actions.click_film(film).select_day(month_day).sleep(1).click_schedule(film, hall, showtime).sleep(1)
        cdp.actions.confirm().sleep(2)
        clpage.actions.join_to_ad_basket().sleep(1).shopping_basket().sleep(1)
        bp = ADBasketPage()
        bp.actions.sleep(2).select_all().sleep(2).click_org_price().sleep(2)
        ConfirmOrderPage().actions.submit().sleep(1)

    @pytest.mark.testcase('我的->我的广告素材：删除按钮功能的正确性 - 我的广告素材界面，点击删除按钮，验证各项显示', author="siwenwei", editor="")
    def test_delete_ad_material(self, testdata):

        ad_name = testdata.get('广告素材名')
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_my_tab().sleep(1)

        mpage = MyselfPage()
        mpage.actions.my_ad().sleep(3)
        p = MyAdListPage()
        p.actions.is_page_self().remove(ad_name).sleep(3).confirm_delete().sleep(3).check_ad_is_exists(ad_name, False, '删除广告({})失败'.format(ad_name)).sleep(2)

    @pytest.mark.testcase('我的->个人资料检查 - 个人资料填写', author="siwenwei", editor="")
    def test_set_nickname(self, testdata):

        name = testdata.get('昵称')
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_my_tab().sleep(1)

        mpage = MyselfPage()
        mpage.actions.userinfo().sleep(3)
        upage = UserInfoPage()
        upage.actions.nickname(name).sleep(1).male().sleep(1)

    @pytest.mark.testcase('debug调试', author="siwenwei", editor="")
    def test_entry_order_menu(self, testdata):

        # brand = testdata.get("类型")
        # url = settings.URLS.get("雨燕管理后台")
        username, password = settings.USERS.get("雨燕管理后台")

        # clp = CinemaListPage()
        # clp.actions.shopping_basket().sleep(1)
        page = ADBasketPage()
        # page.actions.click_schedule_checkbox('新东北影城（海拉尔店）(修亮)','冰雪奇缘2（数字）','研发修亮2厅','2020-07-30','14:00:00').select_all()
        # page.actions.select_all().click_org_price()
        print(page.get_element('view.car').outer_wxml)
        print(page.get_element('view.pay-bottom').outer_wxml)
        return

        ipage = IndexPage(settings.URLS['首页'])  # 进入索引页面 # .find_curr_duration('07月21日 - 07月27日')
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(2).click_form()

        ipage.actions.sleep(1).click_area()
        apage = AreaPage()
        apage.actions.sleep(1).click_city('河南').sleep(2).click_area('郑州市').sleep(2).confirm().sleep(1)

        ipage.actions.sleep(1).click_duration()
        cpage = CalendarPage()
        cpage.actions.click_selected_date_btn().cancel_selected_date('20年', '07/28 - 08/03').sleep(1)
        cpage.actions.select_year('2021年').select_month('2月').select_date('7').click_selected_date_btn().sleep(3).finish().sleep(3)
        ipage.actions.click_make_ad_btn().sleep(1).click_notice_dialog_close_btn().sleep(1).click_select_upload_picture_btn().sleep(2).input_upload_picture_path(r'E:\workspace\upload\code1.jpg').sleep(
            2).screenshot('test_entry_order_menu_剪辑界面_').sleep(3)

        clip_page = ClipPage()
        clip_page.actions.preview().sleep(2).screenshot('test_entry_order_menu_预览界面_').sleep(3)

        ppage = PreviewPage()
        ppage.actions.input_title('autotest_p_009').release().sleep(3).screenshot('test_entry_order_menu_发布界面_').sleep(3).confirm().sleep(10)

        clp = CinemaListPage()
        clp.actions.find_ad_name('at001').find_ad_duration('3s').click_cinema_checkbox('南昌煌泰国际影城').sleep(1).click_cinema_item('南昌煌泰国际影城')

        dp = CinemaDetailPage()
        dp.actions.click_film('冰雪奇缘2（数字）').sleep(1).select_day('07-30').sleep(1).select_day('07-29').sleep(1).click_schedule('冰雪奇缘2（数字）', '陈鹏2厅',
                                                                                                                             '19:00:00').sleep(1).check_total_of_schedule(1, 1).confirm().sleep(1)
        clp.actions.join_to_ad_basket()

        # adb_page = ADBasketPage()
        # adb_page.actions.click_do_ad_btn().sleep(15)

        # opage = OrderPage()
        # opage.actions.click_order_tab().to_be_paid().sleep(1).click_my_tab().sleep(1)

        # mpage = MyselfPage()
        # mpage.actions.click_login().sleep(1)

        # lpage = LoginPage()
        # lpage.actions.check_argee().sleep(1).input_phone_number('18776388419').input_checkcode('12365').login().sleep(15)

        # wlpage = WebLoginPage()
        # wlpage.chrome().maximize_window().open_url(url).actions.input_username(username).input_password(password).input_vcode('at').sleep(2).login().sleep(7)
        # page = HomePage()
        # page.actions.order().sleep(1).order_manager().sleep(2).order_list().sleep(1).orderlist_tab().sleep(1)

        # page.actions.audit().sleep(1).audit_tasklist().sleep(1).audit_tasklist_tab().sleep(7)

        # page1 = AuditTaskListPage()

        # rowinfo = {
        # "taskno": "fcc80dd7e507767ab03a03a0fb0814c5",
        # "adno": "1082",
        # "orderno": "1",
        # "filmno": "1",
        # "status": "审核未通过"
        # }

        # page1.actions.audit_pass().sleep(1).audit_fail().sleep(1).all_audit_tasks().sleep(1).audit_tasknumber("fcc80dd7e507767ab03a03a0fb0814c5").ad_number("1082").click_row(rowinfo).audit(rowinfo).sleep(7)
        # page.actions.data().sleep(2).userlist().sleep(2)
        # p = UserListPage()
        # row = dict(user_id='20',phone='18235329282')
        # p.actions.user_id('20').search().sleep(1).click_row(row).sleep(3).see(row).sleep(10)

        # page.actions.data().sleep(2).ad_place_manage().sleep(2)
        # adp = ADPlaceManagePage()
        # rowinfo = {
        # "ad_place_number":"6",
        # "belong_area":"内蒙古自治区 呼和浩特市",
        # "cinema_name":"新东北影城（海拉尔店）(修亮)",
        # "cinema_type":"普通厅",
        # "film_name":"冰雪奇缘2（数字）",
        # "showtime":"2020-04-09 16:15:00",
        # "duration":"300s",
        # "rest":"300s",
        # }
        # adp.actions.film_name('冰雪奇缘2（数字）').sleep(1).cinema_name('新东北影城（海拉尔店）(修亮)').belong_area('内蒙古自治区 呼和浩特市').search().sleep(3)
        # adp.actions.see(rowinfo).sleep(15)
        # adp.actions.turn_to_page(10).sleep(20)

    def teardown_method(self):

        pass

    def teardown_class(self):

        self.WECHAT_MANAGER.release_minium()
        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
