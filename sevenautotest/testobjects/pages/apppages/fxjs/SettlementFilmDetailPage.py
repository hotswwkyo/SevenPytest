# -*- coding:utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.android.nativekey import AndroidKey
from sevenautotest.utils import helper
from sevenautotest.utils import TestAssert as ta
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators

__author__ = "si wen wei"


class SettlementFilmDetailPage(BasePage):
    """
    中影发行结算->影片信息页面
    """
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def film_info_view(self, locators):
            """影片信息区域
            """

            uia_string = locators.get("影片信息view")  # UiSelector().resourceId("filmInfo")
            return self.page.find_element_by_android_uiautomator(uia_string)

        @property
        @page_element_locators()
        def film_name_view(self, locators):
            """影片名称区域"""

            xpath = locators.get("影片名称view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def show_time_view(self, locators):
            """上映时间区域"""

            xpath = locators.get("上映时间view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            # return self.page.find_element_by_android_uiautomator(xpath, timeout=float(timeout))
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def settlement_box_office_view(self, locators):

            xpath = locators.get("结算票房view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def zhongying_pf_view(self, locators):
            """中影票房view"""

            xpath = locators.get("中影票房view")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def shouri_pf_view(self, locators):
            """首日票房view"""

            xpath = locators.get("首日票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def shouzhoumo__pf_view(self, locators):
            """首周末票房view"""

            xpath = locators.get("首周末票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def qian7tian_pf_view(self, locators):
            """前7天票房view"""

            xpath = locators.get("前7天票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def danrizuigao_pf_view(self, locators):
            """单日最高票房view"""

            xpath = locators.get("单日最高票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def see_more_view(self, locators):
            """查看更多view"""

            xpath = locators.get("查看更多view")
            return self.page.find_element_by_xpath(xpath)

        @page_element_locators()
        def datetime_fx_view(self, locators, film_name):
            """发行有效日期view"""

            xpath = locators.get("发行有效日期view")
            xpath = xpath % film_name
            return self.page.find_element_by_xpath(xpath, parent=self.search_result_area)

        @page_element_locators()
        def film_type_fx_view(self, locators, film_name):
            """发行版本view"""

            xpath = locators.get("发行版本view")
            xpath = xpath % film_name
            return self.page.find_element_by_xpath(xpath, parent=self.search_result_area)

        @property
        @page_element_locators()
        def fx_detail_btn(self, locators):
            """进入发行信息详情页按钮"""

            xpath = locators.get("进入按钮")
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def swipe_to_select_year(self, year, direction="down", distance=70, limit_times=20, current_count=1):
            """选择年

            @param year 目标年份
            @param direction 首次滑动方向 down --- 向下   up --- 向上
            @param distance 每次滑动距离
            @param limit_times 递归次数
            @param current_count 当前递归计数
            """
            selector = self.page.elements.year_selector
            text_before_swipe = selector.get_attribute("text")

            if year == text_before_swipe:
                return self
            if current_count > limit_times:
                msg = "找不到: %s, 请检查" % year
                raise NoSuchElementException(msg)

            def _swipe_year_area(times=1):
                selector.click()
                view = self.sleep(2).page.elements.year_select_area
                x = view.location['x']
                y = view.location['y']
                height = view.size['height']
                width = view.size['width']
                start_x = x + width / 2
                start_y = y + height / 2
                end_x = start_x
                if direction.upper() == "down".upper():
                    end_y = start_y + distance
                else:
                    end_y = start_y - distance
                for n in range(times):
                    self.page.driver.swipe(start_x, start_y, end_x, end_y)
                self.click_confirm_btn()
                self.page.sleep(3)

            _swipe_year_area(1)
            text_after_swipe = selector.get_attribute("text")
            if year == text_after_swipe:
                return self
            if text_before_swipe == text_after_swipe:
                if direction.upper() == "down".upper():
                    direction = "up"
                else:
                    direction = "down"
            else:
                target_year = helper.cutout_prefix_digital(year)
                year_before_swipe = helper.cutout_prefix_digital(text_before_swipe)
                year_after_swipe = helper.cutout_prefix_digital(text_after_swipe)

                if target_year and year_before_swipe and year_after_swipe:
                    t = int(target_year)
                    a = int(year_after_swipe)
                    b = int(year_before_swipe)
                    if a > b:  # 当前方向滑动，数值变大
                        if t < a:  # 目标数值小于a数值，说明需要往数值小的方向滑动，改变方向
                            direction = "up" if direction.upper() == "down".upper() else "down"
                    else:
                        if t > a:
                            direction = "up" if direction.upper() == "down".upper() else "down"
                    _swipe_year_area(abs(t - a))
                    self.page.sleep(1)
            self.swipe_to_select_year(year, direction, distance, limit_times=limit_times, current_count=current_count + 1)
            return self

        def zhongying_pf_equals(self, box_office):
            """中影票房是否正确"""
            expected = box_office
            actual = self.page.elements.zhongying_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def shouri_pf_equals(self, box_office):
            """首日票房是否正确"""
            expected = box_office
            actual = self.page.elements.shouri_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def shouzhoumo_pf_equals(self, box_office):
            """首周末票房是否正确"""
            expected = box_office
            actual = self.page.elements.shouzhoumo__pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def qian7tian_pf_equals(self, box_office):
            """前7天票房是否正确"""
            expected = box_office
            actual = self.page.elements.qian7tian_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def danrizuigao_pf_equals(self, box_office):
            """单日最高票房是否正确"""
            expected = box_office
            actual = self.page.elements.danrizuigao_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def input_film_name(self, film_name):
            """输入影片名称"""

            self.page.elements.film_name_inputbox.clear()
            self.page.elements.film_name_inputbox.send_keys(film_name)
            return self

        def click_confirm_btn(self):
            """点击确定按钮"""

            self.page.elements.confirm_btn.click()
            return self

        def click_cancel_btn(self):
            """点击取消按钮"""

            self.page.elements.cancel_btn.click()
            return self

        def click_search(self):
            self.page.press_keycode(AndroidKey.ENTER)  # SEARCH
            return self

        def click_film_item(self, film_name):
            """点击结算影片项"""
            self.page.elements.film_in_search_result_area(film_name).click()
            return self
