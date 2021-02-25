# -*- coding: utf-8 -*-
import re
import datetime
from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class CalendarPage(BasePage):
    """日历页面"""
    @classmethod
    def join_two_xpath(cls, x1, x2):
        """拼接xpath"""

        slash = '/'
        if x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2[1:]
        elif not x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2
        elif x1.endswith(slash) and not x2.startswith(slash):
            return x1 + x2
        else:
            return x1 + slash + x2

    @classmethod
    def join_xpath(cls, *xpath):

        first = xpath[0]
        others = xpath[1:]
        full_xpath = first
        for x in others:
            full_xpath = cls.join_two_xpath(full_xpath, x)
        return full_xpath

    class Elements(BasePage.Elements):
        @property
        def _fixed_xpath(self):
            """日历区域固定div xpath"""

            p1 = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-calendar-picker-container")]'
            p2 = 'div[contains(@class,"ant-calendar")]/div[contains(@class,"ant-calendar-panel")]'
            return self.page.join_xpath(p1, p2)

        @property
        def current_date(self):
            """当前日期"""

            p1 = 'div[contains(@class,"ant-calendar-input-wrap")]/div[contains(@class,"ant-calendar-date-input-wrap")]/input[contains(@class,"ant-calendar-input ")]'
            return self.page.find_element_by_xpath(self.page.join_xpath(self._fixed_xpath, p1))

        def _header_btn(self, title_prefix, btn_class):
            """日历头部按钮"""

            p1 = 'div[contains(@class,"ant-calendar-date-panel")]/div[contains(@class,"ant-calendar-header")]//a[starts-with(@title,"{title_prefix}") and contains(@class, "{btn_class}")]'.format(
                title_prefix=title_prefix, btn_class=btn_class)
            xpath = self.page.join_xpath(self._fixed_xpath, p1)
            return self.page.find_element_by_xpath(xpath)

        @property
        def previous_year_btn(self):
            """上一年"""

            title_prefix = '上一年'
            btn_class = 'ant-calendar-prev-year-btn'
            return self._header_btn(title_prefix, btn_class)

        @property
        def previous_month_btn(self):
            """上个月"""

            title_prefix = '上个月'
            btn_class = 'ant-calendar-prev-month-btn'
            return self._header_btn(title_prefix, btn_class)

        @property
        def next_year_btn(self):
            """下一年"""

            title_prefix = '下一年'
            btn_class = 'ant-calendar-next-year-btn'
            return self._header_btn(title_prefix, btn_class)

        @property
        def next_month_btn(self):
            """下个月"""

            title_prefix = '下个月'
            btn_class = 'ant-calendar-next-month-btn'
            return self._header_btn(title_prefix, btn_class)

        @property
        def current_year_month(self):
            """当前年月"""

            span_class = 'ant-calendar-ym-select'
            p1 = 'div[contains(@class,"ant-calendar-date-panel")]/div[contains(@class,"ant-calendar-header")]//span[contains(@class, "{span_class}")]'.format(span_class=span_class)
            p2 = 'a[@title="选择年份"]'
            p3 = 'a[@title="选择月份"]'
            year_xpath = self.page.join_xpath(self._fixed_xpath, p1, p2)
            month_xpath = self.page.join_xpath(self._fixed_xpath, p1, p3)
            el_year = self.page.find_element_by_xpath(year_xpath)
            el_month = self.page.find_element_by_xpath(month_xpath)
            return el_year, el_month

        def day_cell(self, year, month, day):
            """几号"""

            table_class = 'ant-calendar-table'
            p1 = 'div[contains(@class,"ant-calendar-date-panel")]/div[contains(@class,"ant-calendar-body")]//table[contains(@class, "{table_class}")]'.format(table_class=table_class)
            p2 = 'tbody/tr/td[@title="{year}年{month}月{day}日"]/div[normalize-space()="{day}"]'.format(year=year, month=month, day=day)
            xpath = self.page.join_xpath(self._fixed_xpath, p1, p2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def today_btn(self):
            """今天"""

            name = '今天'
            p1 = 'div[contains(@class,"ant-calendar-date-panel")]/div[contains(@class,"ant-calendar-body")]//div[contains(@class, "ant-calendar-footer")]/span/a[normalize-space()="{name}"]'.format(name=name)
            xpath = self.page.join_xpath(self._fixed_xpath, p1)
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def previous_year(self):
            """点击 上一年"""

            self.page.elements.previous_year_btn.click()
            return self

        def next_year(self):
            """点击 下一年"""

            self.page.elements.next_year_btn.click()
            return self

        def previous_month(self):
            """点击 上个月"""

            self.page.elements.previous_month_btn.click()
            return self

        def next_month(self):
            """点击 下个月"""

            self.page.elements.next_month_btn.click()
            return self

        def today(self):
            """点击 今天"""

            self.page.elements.today_btn.click()
            return self

        def select_date(self, year, month, day, fmt='%Y-%m-%d'):
            """点选指定日期"""

            year = year if isinstance(year, int) else int(year)
            month = month if isinstance(month, int) else int(month)
            day = day if isinstance(day, int) else int(day)

            target_date = datetime.datetime(year, month, day)
            el_curr_date = self.page.elements.current_date
            if target_date.strftime(fmt) == el_curr_date.get_attribute('value'):
                self.page.elements.day_cell(year, month, day).click()
                return self

            def extract_numbers(text):

                regex = "^(\\d+).*"
                pattern = re.compile(regex)
                matcher = pattern.search(text.strip())
                return int(matcher.group(1)) if matcher else None

            while True:
                el_year, el_month = self.page.elements.current_year_month
                int_curr_year = extract_numbers(el_year.text)
                int_curr_month = extract_numbers(el_month.text)
                if year == int_curr_year and month == int_curr_month:
                    break
                else:
                    if year > int_curr_year:
                        self.next_year()
                    elif year < int_curr_year:
                        self.previous_year()
                    if month > int_curr_month:
                        self.next_month()
                    elif month < int_curr_month:
                        self.previous_month()
            self.page.elements.day_cell(year, month, day).click()
            return self
