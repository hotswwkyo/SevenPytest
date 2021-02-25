# -*- coding:utf-8 -*-
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators


class HomePage(BasePage):
    """
    中影发行结算主页面
    """
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def film_tab(self, locators):
            """下方导航影片tab"""

            xpath = locators.get("影片tab")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def settlement_tab(self, locators):
            """下方导航结算tab"""

            xpath = locators.get("结算tab")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def cinema_tab(self, locators):
            """下方导航影院tab"""

            xpath = locators.get("影院tab")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def my_tab(self, locators):
            """下方导航我的tab"""

            xpath = locators.get("我的tab")
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def click_film_tab(self):
            """点击影片tab"""

            self.page.elements.film_tab.click()
            return self

        def click_settlement_tab(self):
            """点击结算tab"""

            self.page.elements.settlement_tab.click()
            return self

        def click_cinema_tab(self):
            """点击影院tab"""

            self.page.elements.cinema_tab.click()
            return self

        def click_my_tab(self):
            """点击我的tab"""

            self.page.elements.my_tab.click()
            return self
