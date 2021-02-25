# -*- coding:utf-8 -*-
from sevenautotest.utils import helper
from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class CalendarPage(BaseMiniumPage):
    """投放周期日历页面"""
    class Elements(BaseMiniumPage.Elements):
        def calendar_year(self, year):
            """年"""

            selector = 'view.calendar.header'
            inner_text = year
            el_y = self.page.get_element(selector).get_element('view.years').get_element('view.year', inner_text=inner_text)
            outer_wxml = el_y.outer_wxml
            helper.ignore_unused(outer_wxml)
            return el_y

        def calendar_month(self, month):
            """月"""

            selector = 'view.calendar.header'
            inner_text = month
            el_m = self.page.get_element(selector).get_element('view.months').get_element('view.scroll-view').get_element('span.month', inner_text=inner_text)
            outer_wxml = el_m.outer_wxml
            helper.ignore_unused(outer_wxml)
            return el_m

        def calendar_date(self, day):
            """日期区域"""

            selector = 'scroll-view.scroll-view'
            inner_text = day
            el_weeks = self.page.get_element(selector).get_elements('view.calendar>view.week')
            right_el_day = None
            for i, el_week in enumerate(el_weeks):
                if i == 0:
                    continue
                el_days = el_week.get_elements('text')
                for el_day in el_days:
                    if el_day.inner_text.strip() == inner_text:
                        # find element
                        right_el_day = el_day
                        break
                if right_el_day:
                    break

            return right_el_day

        @property
        def selected_date_btn(self):
            """展开已选日期"""

            selector = 'view.select-date'
            inner_text = '展开已选日期'
            el_views = self.page.get_element(selector).get_elements('view')

            elv = None
            for el_view in el_views:
                el_text = el_view.get_element('text', inner_text=inner_text)
                if el_text:
                    elv = el_view
                    break
            el_icon = elv.get_element('text')
            outer_wxml = el_icon.outer_wxml
            helper.ignore_unused(outer_wxml)
            return el_icon

        @property
        def total_btn(self):
            """ 共计   天"""

            selector = 'view.button'
            inner_text = '完成'
            btns = self.page.get_elements(selector)
            right_el_total = None
            for btn in btns:
                el_total = btn.get_element('text')
                itext = el_total.inner_text.strip()
                if itext.startswith('共计') and itext.endswith('天') and btn.inner_text.strip().endswith(inner_text):
                    right_el_total = el_total
                    break
            outer_wxml = right_el_total.outer_wxml
            helper.ignore_unused(outer_wxml)
            return right_el_total

        @property
        def finish_btn(self):
            """完成按钮"""

            selector = 'view.button'
            inner_text = '完成'
            btns = self.page.get_elements(selector)
            el_btn = None
            for btn in btns:
                if btn.get_element('text').inner_text.strip().startswith('共计') and btn.inner_text.strip().endswith(inner_text):
                    el_btn = btn
                    break
            outer_wxml = el_btn.outer_wxml
            helper.ignore_unused(outer_wxml)
            return el_btn

        def selected_date(self, short_year, day):
            """已选中日期区域中查找选中的日期"""

            selector = 'view.select-date'
            inner_text = day
            year_day_spaces = self.page.get_element(selector).get_element('view.parseDate').get_elements('view.dates')
            el_dayrows = []
            for year_day_space in year_day_spaces:
                el_year_text = year_day_space.get_element('text.title')
                if el_year_text.inner_text == short_year:
                    el_dayrows = year_day_space.get_elements('view.rows')
                    break
            el_day_icon = None
            for el_dayrow in el_dayrows:
                el_day_text = el_dayrow.get_element('text.date', inner_text=inner_text)
                if el_day_text:
                    el_day_icon = el_dayrow.get_element('mp-icon')
                    break
            if not el_day_icon:
                self.page.raise_error('找不到符合条件的元素: {} {}'.format(short_year, day))
            return el_day_icon

        @property
        def all_selected_days(self):
            """已选中日期区域中的所有日期"""

            selector = 'view.select-date'
            year_day_spaces = self.page.get_element(selector).get_elements('view.parseDate>view.dates')
            year_and_days_list = []
            for year_day_space in year_day_spaces:
                el_year_text = year_day_space.get_element('text.title')
                if el_year_text:
                    el_days = year_day_space.get_elements('view.rows>text.date')
                    year_and_days_list.append((el_year_text, el_days))
            return year_and_days_list

    class Actions(BaseMiniumPage.Actions):
        def select_year(self, year):
            """ 选择年 """

            self.page.elements.calendar_year(year).click()
            return self

        def select_month(self, month):
            """ 选择月 """

            self.page.elements.calendar_month(month).click()
            return self

        def select_date(self, date):
            """ 选择日期 """

            self.page.elements.calendar_date(date).click()
            return self

        def click_selected_date_btn(self):
            """ 点击 展开已选日期 """

            self.page.elements.selected_date_btn.click()
            return self

        def finish(self):
            """ 点击 完成按钮 """

            self.page.elements.finish_btn.click()
            return self

        def cancel_selected_date(self, short_year, date):
            """ 展开已选日期区域中取消选中日期 """

            self.page.elements.selected_date(short_year, date).click()
            return self

        def check_selected_total_days(self, total_days):
            """ 检查已选择的总天数 """

            itext = self.page.elements.total_btn.inner_text.strip()
            ntext = itext.strip("共计").strip('天').strip()
            a_days = int(ntext)
            e_days = int(total_days)
            if a_days != e_days:
                raise AssertionError("预期(共计 {e} 天) != 实际(共计 {a} 天)".format(e=e_days, a=a_days))
            return self

        def check_selected_is_exists(self, *year_and_daylist):
            """检查在底部已选择日期区域是否存在预期的日期

            Args:
                year_and_daylist: [['20年',['08/05', '08/06',...]],...]
            """

            el_days = self.page.elements.all_selected_days
            for one in year_and_daylist:
                year = one[0]
                daylist = one[1]
                self._find_days_in_selected_days(el_days, year, *tuple(daylist))
            return self

        def _find_days_in_selected_days(self, el_selected_days, short_year, *days):

            not_found_days = []
            find_year = False
            all_years = []
            all_days = []
            for el_year, el_day_list in el_selected_days:
                year_str = el_year.inner_text
                all_years.append(year_str)
                if year_str == short_year:
                    find_year = True
                    all_days = [el_day.inner_text for el_day in el_day_list]
                    for day in days:
                        if day not in all_days:
                            not_found_days.append(day)
                    break
            if not find_year:
                self.page.fail('找不到年({}),选中区域中显示的年如下：{}'.format(short_year, ', '.join(all_years)))
            if not_found_days:
                fmt = '找不到{year}以下日期：{not_found_days}，选中区域中显示的{year}的日期如下：{all_days}'
                msg = fmt.format(not_found_days=', '.join(not_found_days), year=short_year, all_days=', '.join(all_days))
                self.page.fail(msg)
