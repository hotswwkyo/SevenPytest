# -*- coding:utf-8 -*-
"""

"""
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.basetestcase import BaseTestCase

from sevenautotest.testobjects.pages.webpages.yy.login_page import LoginPage as WebLoginPage
from sevenautotest.testobjects.pages.webpages.yy.home_page import HomePage
from sevenautotest.testobjects.pages.webpages.yy.userlist_page import UserListPage
from sevenautotest.testobjects.pages.webpages.yy.user_edit_page import UserEditPage
from sevenautotest.testobjects.pages.webpages.yy.haoyou_zhuli_page import HaoYouZhuLiPage
from sevenautotest.testobjects.pages.webpages.yy.haoyou_zhuli_activity_detail_page import HaoYouZhuLiActivityDetailPage


class BackstageUserlistTest(BaseTestCase):
    """ 管理后台用户列表测试 """
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

    @pytest.mark.testcase('用户列表查询 - 用户ID输入正确且存在的用户ID', author="siwenwei", editor="")
    def test_search_with_right_userid(self, testdata):

        userid = testdata.get("用户ID")
        phone = testdata.get("手机号")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        rowinfo = {
            "user_id": userid,
            "phone": phone,
        }

        ul_page.actions.user_id(userid).sleep(1).search().sleep(3).check_userlist_table(rowinfo, check_total=True)

    @pytest.mark.testcase('用户列表查询 - 用户ID输入错误的不存在的用户ID', author="siwenwei", editor="")
    def test_search_with_wrong_or_notexists_userid(self, testdata):

        userid = testdata.get("用户ID")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).search().sleep(3)
        if not ul_page.actions.is_empty_table():
            tips = '使用错误的不存在的用户ID({userid})能查询出数据'
            self.fail(tips.format(userid=userid))

    @pytest.mark.testcase('用户列表查询 - 手机号输入正确且存在的手机号', author="siwenwei", editor="")
    def test_search_with_right_phone_number(self, testdata):

        userid = testdata.get("用户ID")
        phone = testdata.get("手机号")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        rowinfo = {"user_id": userid, "phone": phone, 'user_alias': alias}
        ul_page.actions.phone_number(phone).sleep(1).search().sleep(3).check_userlist_table(rowinfo)

    @pytest.mark.testcase('用户列表查询 - 手机号输入错误的不存在的手机号', author="siwenwei", editor="")
    def test_search_with_wrong_phone_number(self, testdata):

        phone = testdata.get("手机号")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.phone_number(phone).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 手机号输入存在的手机号的部分字段', author="siwenwei", editor="")
    def test_search_with_parttext_phone_number(self, testdata):

        phone = testdata.get("手机号(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.phone_number(phone).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list, check_total=True)

    @pytest.mark.testcase('用户列表查询 - 手机号输入特殊字符', author="siwenwei", editor="")
    def test_search_with_phone_number_which_has_special_characters(self, testdata):

        phone = testdata.get("手机号")
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.phone_number(phone).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户昵称输入正确且存在的用户昵称', author="siwenwei", editor="")
    def test_search_with_right_alias(self, testdata):

        userid = testdata.get("用户ID")
        phone = testdata.get("手机号")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        rowinfo = {"user_id": userid, "phone": phone, 'user_alias': alias}
        ul_page.actions.user_alias(alias).sleep(1).search().sleep(3).check_userlist_table(rowinfo)

    @pytest.mark.testcase('用户列表查询 - 用户昵称输入错误的不存在的用户昵称', author="siwenwei", editor="")
    def test_search_with_wrong_or_notexists_alias(self, testdata):

        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_alias(alias).sleep(1).search().sleep(3)
        if not ul_page.actions.is_empty_table():
            tips = '使用错误的不存在的用户昵称({alias})能查询出数据'
            self.fail(tips.format(alias=alias))

    @pytest.mark.testcase('用户列表查询 - 用户昵称输入存在的用户昵称的部分字段', author="siwenwei", editor="")
    def test_search_with_parttext_alias(self, testdata):

        salias = testdata.get("用户昵称(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_alias(salias).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户列表查询 - 用户昵称输入特殊字符', author="siwenwei", editor="")
    def test_search_with_special_characters(self, testdata):

        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_alias(alias).sleep(1).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户ID和用户昵称组合输入正确的用户ID和错误的用户昵称', author="siwenwei", editor="")
    def test_search_with_right_userid_and_wrong_alias(self, testdata):

        userid = testdata.get("用户ID")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).user_alias(alias).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户ID和用户昵称组合输入错误的用户ID和正确用户昵称', author="siwenwei", editor="")
    def test_search_with_wrong_userid_and_right_alias(self, testdata):

        userid = testdata.get("用户ID")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).user_alias(alias).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户ID和用户昵称组合输入错误的用户ID和用户昵称', author="siwenwei", editor="")
    def test_search_with_wrong_userid_and_alias(self, testdata):

        userid = testdata.get("用户ID")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).user_alias(alias).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户ID和用户昵称等输入特殊符号点击查询', author="siwenwei", editor="")
    def test_search_with_special_characters_userid_and_alias(self, testdata):

        userid = testdata.get("用户ID")
        alias = testdata.get("用户昵称")

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).user_alias(alias).search().sleep(3).is_empty_table()

    @pytest.mark.testcase('用户列表查询 - 用户ID和用户昵称输入内容的时候重置', author="siwenwei", editor="")
    def test_input_is_clear_when_click_reset_after_input_content(self, testdata):

        userid = testdata.get("用户ID")
        alias = testdata.get("用户昵称")
        empty = ''
        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_id(userid).sleep(1).user_alias(alias).sleep(1).reset().sleep(3)
        if ul_page.elements.user_id.text != empty or ul_page.elements.user_alias.text != empty:
            tips = '重置失败'
            self.fail(tips)

    @pytest.mark.testcase('生命周期查询导入期', author="siwenwei", editor="")
    def test_search_with_daoru_lifecycle(self, testdata):

        lcf = testdata.get("生命周期标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.lifecycle(lcf).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('生命周期查询成长期', author="siwenwei", editor="")
    def test_search_with_chengzhang_lifecycle(self, testdata):

        lcf = testdata.get("生命周期标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.lifecycle(lcf).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('生命周期查询成熟期', author="siwenwei", editor="")
    def test_search_with_chengshu_lifecycle(self, testdata):

        lcf = testdata.get("生命周期标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.lifecycle(lcf).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('生命周期查询休眠期', author="siwenwei", editor="")
    def test_search_with_xiumian_lifecycle(self, testdata):

        lcf = testdata.get("生命周期标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.lifecycle(lcf).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('生命周期查询流失期', author="siwenwei", editor="")
    def test_search_with_liushi_lifecycle(self, testdata):

        lcf = testdata.get("生命周期标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.lifecycle(lcf).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户特殊属性标签查询KOL用户', author="siwenwei", editor="")
    def test_search_with_kol_attribute(self, testdata):

        flag = testdata.get("用户特殊属性标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_special_attr(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户特殊属性标签查询活跃用户', author="siwenwei", editor="")
    def test_search_with_huoyue_attribute(self, testdata):

        flag = testdata.get("用户特殊属性标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_special_attr(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户特殊属性标签查询购买粘性用户', author="siwenwei", editor="")
    def test_search_with_nianxing_attribute(self, testdata):

        flag = testdata.get("用户特殊属性标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_special_attr(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户特殊属性标签查询高单价用户', author="siwenwei", editor="")
    def test_search_with_gaodanjia_attribute(self, testdata):

        flag = testdata.get("用户特殊属性标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_special_attr(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户特殊属性标签查询回流用户', author="siwenwei", editor="")
    def test_search_with_huiliu_attribute(self, testdata):

        flag = testdata.get("用户特殊属性标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.user_special_attr(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户类型标签查询商户用户 2020-09-23', author="siwenwei", editor="")
    def test_search_with_shanghu(self, testdata):

        flag = testdata.get("用户类型标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.usertype(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('用户类型标签查询个人用户 2020-09-23', author="siwenwei", editor="")
    def test_search_with_geren(self, testdata):

        flag = testdata.get("用户类型标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        ul_page.actions.usertype(flag).sleep(1).search().sleep(3)

        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('修改用户类型由商户变为个人后，以个人类型进行查询测试 2020-09-23', author="siwenwei", editor="")
    def test_search_with_geren_after_change_shanghu_to_geren(self, testdata):

        flag = testdata.get("用户类型标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        editrows = helper.group_by_suffix_regex(testdata, r"\(修改行\)$", True)
        editrow = {
            "user_id": editrows[0].get("用户ID"),
        }
        ul_page.actions.edit(editrow)
        editor = UserEditPage()
        editor.actions.sleep(2).personal().submit()
        ul_page.actions.sleep(1).usertype(flag).sleep(1).search().sleep(3)
        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    @pytest.mark.testcase('修改用户A用户类型由商户用户变为个人用户，再改回商户用户查询查询 2020-09-23', author="siwenwei", editor="")
    def test_search_with_shanghu_after_change_geren_to_shanghu(self, testdata):

        home_page = HomePage()
        home_page.actions.sleep(1).spread().sleep(1).haoyouzhuli().sleep(2)
        hypage = HaoYouZhuLiPage()
        rowinfo = dict(activity_code='467dbea71ec9d3ef328fddbe5514d895', activity_status='进行中', activity_cycle='2020-08-20 00:00 至 2020-09-30 11:03', real_end_time='', help_sponsors='3', new_add_users='4')
        hypage.actions.sleep(3).detail(rowinfo).sleep(7)
        dpage = HaoYouZhuLiActivityDetailPage()
        info = {
            'user_number': '16',
            'alias': '大伟',
            'phone': '17368839772',
            'friends_total': '1',
            'coupon_code_number': '23',
            'discount': '88',
            'first_share_time': '2020-08-25 10:42:39',
        }
        dpage.actions.user_number('16').phone_number('17368839772').search().check_friends_table(info).sleep(3)
        cat = {
            'activity_code': '467dbea71ec9d3ef328fddbe5514d895',
            'activity_status': '2',
            'start_time': '2020-08-20 00:00',
            'end_time': '2020-09-30 11:03',
        }
        dpage.actions.check_activity_table(cat)
        ort = {
            'create_time': '2020-08-20 11:03:36',
            'activity_code': '467dbea71ec9d3ef328fddbe5514d895',
            'action': '添加活动',
            'operator': 'admin',
        }
        dpage.actions.click_operation_record_table_row(ort).sleep(10)
        return

        flag = testdata.get("用户类型标签(查询)")
        fixed = "预期_"
        suffix_regex = r"\({}\d+\)$".format(fixed)

        home_page = HomePage()
        home_page.actions.sleep(1).data().sleep(1).userlist().sleep(2)

        ul_page = UserListPage()
        editrows = helper.group_by_suffix_regex(testdata, r"\(修改行\)$", True)
        editrow = {
            "user_id": editrows[0].get("用户ID"),
        }
        ul_page.actions.edit(editrow)
        editor = UserEditPage()
        editor.actions.sleep(2).select_usertype('个人').sleep(1).submit()
        ul_page.actions.sleep(3).edit(editrow)
        editor.actions.sleep(2).select_usertype('商户').sleep(1).submit()

        ul_page.actions.sleep(1).usertype(flag).sleep(1).search().sleep(3)
        e_userinfo_list = helper.group_by_suffix_regex(testdata, suffix_regex, True, helper.digital_suffix_cmp_wrapper(lambda suffix: suffix.lstrip("(").rstrip(")")[len(fixed):]))
        rowinfo_list = []
        for e_userinfo in e_userinfo_list:
            rowinfo = {"user_id": e_userinfo.get("用户ID"), "phone": e_userinfo.get("手机号"), 'user_alias': e_userinfo.get("用户昵称")}
            rowinfo_list.append(rowinfo)
        ul_page.actions.check_userlist_table(rowinfo_list)

    def teardown_method(self):

        pass

    def teardown_class(self):

        # self.WECHAT_MANAGER.release_minium()
        self.DRIVER_MANAGER.close_all_drivers()


if __name__ == "__main__":
    pass
