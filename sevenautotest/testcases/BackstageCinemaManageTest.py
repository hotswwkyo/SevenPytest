# -*- coding:utf-8 -*-
"""

"""
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.webpages.yy.login_page import LoginPage as WebLoginPage
from sevenautotest.testobjects.pages.webpages.yy.home_page import HomePage
from sevenautotest.testobjects.pages.webpages.yy.cinema_manage_page import CinemaManagePage


class BackstageCinemaManageTest(BaseTestCase):
    """ 管理后台影院管理测试 """
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

    @pytest.mark.testcase('影院列表查询 - 影院编码框输入存在的影院的编码查询', author="siwenwei", editor="")
    def test_search_cinema_with_right_cienma_number(self, testdata):

        code_number = testdata.get("影院编码(查询)")
        cinema_name = testdata.get("影院名称")
        status = testdata.get("影院状态")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        rowinfo = {
            "code_number": code_number,
            "cinema_name": cinema_name,
            "status": status,
        }
        cm_page.actions.sleep(3).cinema_code(code_number).sleep(1).search().sleep(3).check_cinema_table(rowinfo, check_total=True).sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影院列表查询 - 影院编码框输入存在的影院的编码部分字段查询', author="siwenwei", editor="")
    def test_search_cinema_with_part_cienma_number(self, testdata):

        scode_number = testdata.get("影院编码(查询)")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_code(scode_number).sleep(1).search().sleep(3).is_empty_cinema_table().sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影院列表查询 - 影院编码框输入不存在的影院的编码查询', author="siwenwei", editor="")
    def test_search_cinema_with_wrong_cienma_number(self, testdata):

        scode_number = testdata.get("影院编码(查询)")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_code(scode_number).sleep(1).search().sleep(3).is_empty_cinema_table().sleep(1)

    @pytest.mark.testcase('影院列表查询 - 影院名称框输入存在的影院的名称查询', author="siwenwei", editor="")
    def test_search_cinema_with_right_cienma_name(self, testdata):

        scinema_name = testdata.get("影院名称(查询)")
        code_number = testdata.get("影院编码")
        cinema_name = testdata.get("影院名称")
        status = testdata.get("影院状态")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2).ad_place_manage().sleep(2)

        cm_page = CinemaManagePage()
        rowinfo = {
            "code_number": code_number,
            "cinema_name": cinema_name,
            "status": status,
        }
        cm_page.actions.sleep(3).cinema_name(scinema_name).sleep(1).search().sleep(3).check_cinema_table(rowinfo, check_total=True).sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影院列表查询 - 影院名称框输入存在的影院的名称部分字段查询', author="siwenwei", editor="")
    def test_search_cinema_with_part_cienma_name(self, testdata):

        cinema_name = testdata.get("影院名称(查询)")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_name(cinema_name).sleep(1).search().sleep(3).is_empty_cinema_table().sleep(1)

    # todo 查询功能未完成，等待完成后进行调试
    @pytest.mark.testcase('影院列表查询 - 影院名称框输入不存在的影院的名称查询', author="siwenwei", editor="")
    def test_search_cinema_with_wrong_cienma_name(self, testdata):

        cinema_name = testdata.get("影院名称(查询)")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_name(cinema_name).sleep(1).search().sleep(3).is_empty_cinema_table().sleep(1)

    @pytest.mark.testcase('影院列表查询 - 所属地区省输入已有数据存在的省份', author="siwenwei", editor="")
    def test_search_cinema_with_province_which_has_cinemas(self, testdata):

        p = testdata.get("省份(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        expected_rows = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        all_rowinfo = []
        for expected_row in expected_rows:
            all_rowinfo.append({
                "code_number": expected_row.get("影院编码"),
                "cinema_name": expected_row.get("影院名称"),
                "status": expected_row.get("影院状态"),
                "belong": expected_row.get("所属地区"),
            })
        cm_page.actions.sleep(3).province(p).sleep(1).search().sleep(3).check_cinema_table(*all_rowinfo, check_total=True).sleep(1)

    @pytest.mark.testcase('影院列表查询 - 所属地区省输入已有数据不存在的省份', author="siwenwei", editor="")
    def test_search_cinema_with_province_which_no_cinemas(self, testdata):

        p = testdata.get("省份(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).province(p).sleep(1).search().sleep(3).is_empty_cinema_table()

    @pytest.mark.testcase('影院列表查询 - 选省，所属地区市选择已有数据存在的市', author="siwenwei", editor="")
    def test_search_cinema_with_city_which_has_cinemas(self, testdata):

        p = testdata.get("省份(查询)")
        c = testdata.get("城市(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        expected_rows = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        all_rowinfo = []
        for expected_row in expected_rows:
            all_rowinfo.append({
                "code_number": expected_row.get("影院编码"),
                "cinema_name": expected_row.get("影院名称"),
                "status": expected_row.get("影院状态"),
                "belong": expected_row.get("所属地区"),
            })
        cm_page.actions.sleep(3).province(p).sleep(3).city(c).sleep(1).search().sleep(3).check_cinema_table(*all_rowinfo, check_total=True).sleep(1)

    @pytest.mark.testcase('影院列表查询 - 选省，所属地区市选择已有数据不存在的市', author="siwenwei", editor="")
    def test_search_cinema_with_city_which_no_cinemas(self, testdata):

        p = testdata.get("省份(查询)")
        c = testdata.get("城市(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)
        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).province(p).sleep(3).city(c).sleep(1).search().sleep(3).is_empty_cinema_table()

    @pytest.mark.testcase('影院列表查询 - 影院编码、影院名称框输入存在的影院名称或者编码，地区输入不匹配的省/市', author="siwenwei", editor="")
    def test_search_cinema_with_mismatched_area_and_other_is_right(self, testdata):

        code = testdata.get("影院编码(查询)")
        name = testdata.get("影院名称(查询)")
        p = testdata.get("省份(查询)")
        c = testdata.get("城市(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)
        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_name(name).cinema_code(code).province(p).sleep(3).city(c).sleep(1).search().sleep(3).is_empty_cinema_table()

    @pytest.mark.testcase('影院列表查询 - 影院编码、影院名称框输入不存在的影院名称或者编码，地区输入具体的省/市', author="siwenwei", editor="")
    def test_search_cinema_with_matched_area_and_other_is_wrong(self, testdata):

        code = testdata.get("影院编码(查询)")
        name = testdata.get("影院名称(查询)")
        p = testdata.get("省份(查询)")
        c = testdata.get("城市(查询)")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)
        cm_page = CinemaManagePage()
        cm_page.actions.sleep(3).cinema_name(name).cinema_code(code).province(p).sleep(3).city(c).sleep(1).search().sleep(3).is_empty_cinema_table()

    @pytest.mark.testcase('影院列表查询 - 影院编码、影院名称框输入存在的影院名称或者编码，地区输入匹配的省/市 2020-09-07', author="siwenwei", editor="")
    def test_search_cinema_with_all_right_items(self, testdata):

        code = testdata.get("影院编码(查询)")
        name = testdata.get("影院名称(查询)")
        p = testdata.get("省份(查询)")
        c = testdata.get("城市(查询)")
        suffix_regex = r"\(\d+\)$"
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).cinema_manage().sleep(2)

        cm_page = CinemaManagePage()
        expected_rows = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")))
        all_rowinfo = []
        for expected_row in expected_rows:
            all_rowinfo.append({
                "code_number": expected_row.get("影院编码"),
                "cinema_name": expected_row.get("影院名称"),
                "status": expected_row.get("影院状态"),
                "belong": expected_row.get("所属地区"),
            })
        cm_page.actions.sleep(3).cinema_name(name).cinema_code(code).province(p).sleep(3).city(c).sleep(1).search().sleep(3).check_cinema_table(*all_rowinfo, check_total=True).sleep(1)

    def teardown_method(self):

        pass

    def teardown_class(self):

        # self.WECHAT_MANAGER.release_minium()
        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
