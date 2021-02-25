# -*- coding:utf-8 -*-
"""

"""
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.basetestcase import BaseTestCase

from sevenautotest.testobjects.pages.webpages.yy.login_page import LoginPage as WebLoginPage
from sevenautotest.testobjects.pages.webpages.yy.home_page import HomePage
from sevenautotest.testobjects.pages.webpages.yy.film_manage_page import FilmManagePage


class BackstageFilmManageTest(BaseTestCase):
    """ 管理后台影片管理测试 """
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

    @pytest.mark.testcase('影片列表查询 - 影片名称框输入存在的影片的名称查询', author="siwenwei", editor="")
    def test_search_film_with_right_film_name(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")
        film_name = testdata.get("影片名称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)

        fm_page = FilmManagePage()
        rowinfo = {
            "film_name": film_name,
        }
        fm_page.actions.sleep(3).film_name(sfilm_name).sleep(1).search().sleep(3).check_film_list_table(rowinfo, check_total=True).sleep(1)

    @pytest.mark.testcase('影片列表查询 - 影片名称框输入存在的影片的名称部分字段查询', author="siwenwei", editor="")
    def test_search_film_with_part_film_name(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)

        fm_page = FilmManagePage()
        expected_films = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        rowinfo_list = []
        for expected_film in expected_films:
            fname = expected_film.get("影片名称")
            if fname is not None:
                rowinfo_list.append({
                    "film_name": fname,
                })
        fm_page.actions.sleep(3).film_name(sfilm_name).sleep(1).search().sleep(3).check_film_list_table(*rowinfo_list, check_total=True).sleep(1)

    @pytest.mark.testcase('影片列表查询 - 影片名称框输入不存在的影片的名称字段查询', author="siwenwei", editor="")
    def test_search_film_with_noexists_film_name(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).film_name(sfilm_name).sleep(1).search().sleep(3).is_empty_film_list_table()
        self.sleep(1)

    @pytest.mark.testcase('影片列表查询 - 影片名称框输入特殊字符查询', author="siwenwei", editor="")
    def test_search_film_with_special_chart_name(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).film_name(sfilm_name).sleep(1).search().sleep(3).is_empty_film_list_table()
        self.sleep(1)

    # 页面未显示影片类型，等待调试
    @pytest.mark.testcase('影片列表查询 - 影片类型框输入存在的影片类型查询', author="siwenwei", editor="")
    def test_search_film_with_right_film_type(self, testdata):

        sfilm_type = testdata.get("影片类型(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)

        fm_page = FilmManagePage()
        expected_films = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        rowinfo_list = []
        for expected_film in expected_films:
            fname = expected_film.get("影片名称")
            ftype = expected_film.get("影片类型")
            if fname is not None:
                rowinfo_list.append({
                    "film_name": fname,
                    "film_type": ftype,
                })
        fm_page.actions.sleep(3).film_type(sfilm_type).sleep(1).search().sleep(3).check_film_list_table(*rowinfo_list, check_total=True).sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 影片类型框输入存在的影片类型部分字段查询', author="siwenwei", editor="")
    def test_search_film_with_part_film_type(self, testdata):

        sfilm_type = testdata.get("影片类型(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).film_type(sfilm_type).sleep(1).search().sleep(3).is_empty_film_list_table()
        self.sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 影片类型框输入不存在的影片类型字段查询', author="siwenwei", editor="")
    def test_search_film_with_noexists_film_type(self, testdata):

        sfilm_type = testdata.get("影片类型(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).film_type(sfilm_type).sleep(1).search().sleep(3).is_empty_film_list_table()
        self.sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 影片类型框输入特殊字符查询', author="siwenwei", editor="")
    def test_search_film_with_special_chart_of_type(self, testdata):

        sfilm_type = testdata.get("影片类型(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).film_type(sfilm_type).sleep(1).search().sleep(3).is_empty_film_list_table()
        self.sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 上映日期框选择存在影片的正确上映日期', author="siwenwei", editor="")
    def test_search_film_with_right_showtime(self, testdata):

        sshowtime = testdata.get("上映时间(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        expected_films = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        rowinfo_list = []
        for expected_film in expected_films:
            fname = expected_film.get("影片名称")
            showtime = expected_film.get("上映时间")
            if fname is not None:
                rowinfo_list.append({
                    "film_name": fname,
                    "showtime": showtime,
                })
        fm_page.actions.sleep(3).showtime(sshowtime).sleep(1).search().sleep(3).check_film_list_table(*rowinfo_list)
        self.sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 上映日期框选择存在影片的不匹配的上映日期', author="siwenwei", editor="")
    def test_search_film_with_showtime_of_no_movie(self, testdata):

        sshowtime = testdata.get("上映时间(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(3).showtime(sshowtime).sleep(1).search().sleep(3).is_empty_film_list_table()

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 影片名称、影片类型、上映日期输入同时匹配已有影片A正确内容', author="siwenwei", editor="")
    def test_search_film_with_right_film_name_and_type_and_showtime(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")
        sfilm_type = testdata.get("影片类型(查询)")
        sshowtime = testdata.get("上映时间(查询)")
        film_name = testdata.get("影片名称(预期)")
        film_type = testdata.get("影片类型(预期)")
        showtime = testdata.get("上映日期(预期)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(2).film_name(sfilm_name).sleep(1).film_type(sfilm_type).showtime(sshowtime).sleep(1).search().sleep(3).check_film_list_table(
            {
                'film_name': film_name,
                'film_type': film_type,
                'showtime': showtime,
            }, check_total=True).sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影片列表查询 - 影片名称、影片类型、上映日期输入不同时匹配已有影片A正确内容', author="siwenwei", editor="")
    def test_search_film_with_one_of_all_is_wrong(self, testdata):

        sfilm_name = testdata.get("影片名称(查询)")
        sfilm_type = testdata.get("影片类型(查询)")
        sshowtime = testdata.get("上映时间(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).film_manage().sleep(2)
        fm_page = FilmManagePage()
        fm_page.actions.sleep(2).film_name(sfilm_name).sleep(1).film_type(sfilm_type).showtime(sshowtime).sleep(1).search().sleep(3).is_empty_film_list_table()

    def teardown_method(self):

        pass

    def teardown_class(self):

        # self.WECHAT_MANAGER.release_minium()
        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
