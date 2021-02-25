# -*- coding:utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.android.nativekey import AndroidKey

from sevenautotest.utils import helper
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators


class SettlementMainPage(BasePage):
    """
    中影发行结算主页面
    """
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def my_films(self, locators):
            """我管理影片"""

            xpath = locators.get("我管理影片")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def all_films(self, locators):
            """全部影片"""

            xpath = locators.get("全部影片")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def year_selector(self, locators):
            """年选择列表"""

            xpath = locators.get("年")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            # return self.page.find_element_by_android_uiautomator(xpath, timeout=float(timeout))
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def year_select_area(self, locators):
            xpath = locators.get("年滚动选择区域")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def film_name_inputbox(self, locators):
            """影片名称输入框"""

            xpath = locators.get("影片名")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def years_listbox(self, locators):
            """年滑动选择列表"""

            xpath = locators.get("年")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def confirm_btn(self, locators):
            """确定按钮"""

            xpath = locators.get("确定")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def cancel_btn(self, locators):
            """取消按钮"""

            xpath = locators.get("取消")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def search_result_area(self, locators):
            """查询结果列表"""

            xpath = locators.get("查询结果列表")
            return self.page.find_element_by_xpath(xpath)

        @page_element_locators()
        def film_in_search_result_area(self, locators, film_name):
            """查询结果列表中的影片"""

            xpath = locators.get("查询结果列表中的影片")
            xpath = xpath % film_name
            return self.page.find_element_by_xpath(xpath, parent=self.search_result_area)

    class Actions(BasePage.Actions):
        def click_my_films(self):
            self.page.elements.my_films.click()
            return self

        def click_all_films(self):
            self.page.elements.all_films.click()
            return self

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
