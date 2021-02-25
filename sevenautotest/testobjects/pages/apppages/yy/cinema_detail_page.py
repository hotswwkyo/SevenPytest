# -*- coding:utf-8 -*-
import re
from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class CinemaDetailPage(BaseMiniumPage):
    """影院列表页面"""
    def get_total_of_schedule(self, total_data_text):
        """获取已选择排期场数"""

        regex = '共选中(\\d+)天，(\\d+)场排期$'
        pattern = re.compile(regex)
        matcher = pattern.search(total_data_text)
        if matcher:
            return (matcher.group(1), matcher.group(2))
        else:
            return None

    class Elements(BaseMiniumPage.Elements):
        @property
        def cinema_name(self):
            """影院信息 - 名称"""

            selector = 'view.page-content>view.page-item.cimema-info>view>view.cinema-name'
            return self.page.get_element(selector)

        @property
        def cinema_address(self):
            """影院信息 - 地址"""

            selector = 'view.page-content>view.page-item.cimema-info>view>view.cinema-address'
            return self.page.get_element(selector)

        @property
        def select_all_film_checkbox(self):
            """影片全选复选框"""

            s1 = 'view.page-content>view.film-content>scroll-view.scroll-view-film'
            s2 = 'view>view.film-select>view.film-all-select>image'
            return self.page.get_element(s1).get_element(s2)

        def film_checkbox(self, film):
            """影片复选框"""

            inner_text = film
            s1 = 'view.page-content>view.film-content>scroll-view.scroll-view-film'
            s2 = 'view>view>view.cimema-film-item'
            s3 = 'view.film-view>view.film-title'
            s4 = 'view.film-view>view.film-view-select>image'
            el_scroll = self.page.get_element(s1)
            el_items = el_scroll.get_elements(s2)
            el_checkbox = None
            el_image = None
            for el_item in el_items:
                el_checkbox = el_item.get_element(s3, inner_text=inner_text)
                if el_checkbox:
                    el_image = el_item.get_element(s4)
                    break
            return (el_checkbox, el_image)

        def cinema_day(self, day):
            """影院日期"""

            s1 = 'view.page-content>view.page-item.cimema-day>scroll-view.scroll-view'
            s2 = 'view>view.cimema-day-item>view.text-view>view.day'
            el_scroll = self.page.get_element(s1)
            el_day = el_scroll.get_element(s2, inner_text=day)
            return el_day

        @property
        def select_all_schedule_checkbox(self):
            """全选当日排期复选框"""

            inner_text = '全选当日排期'
            s1 = 'view.page-content>view.page-item.day-all'
            el_views = self.page.get_elements(s1)
            el_checkbox = None
            for el_view in el_views:
                el_text = el_view.get_element('view.cinema-selectText', inner_text=inner_text)
                if el_text:
                    el_checkbox = el_view.get_element('view.cinema-select')
                    if el_checkbox:
                        break
            return el_checkbox

        def film_schedule_checkbox(self, film_name, hall_name, showtime):
            """影片排期复选框"""

            s1 = 'view.page-content>view.film-schedule>view.film-schedule-content>view.film-schedule-item'
            prefix = 'view.film-schedule-info>view.schedule-info-detail'

            fs = prefix + '>' + 'view.schedule-info-item.schedule-info-item-top>text.schedule-info-detail-name'
            ss = prefix + '>' + 'view.schedule-info-item.schedule-info-item-bottom>text.schedule-info-detail-time'
            hs = prefix + '>' + 'view.schedule-info-item.schedule-info-item-bottom>text.schedule-info-detail-hall'

            el_checkbox = None
            el_items = self.page.get_elements(s1)
            for el_item in el_items:
                el_film = el_item.get_element(fs, inner_text=film_name)
                el_hall = el_item.get_element(hs).get_element('text', inner_text=hall_name)
                el_showtime = el_item.get_element(ss)
                if el_film and el_showtime.inner_text.strip() == showtime and el_hall:
                    el_checkbox = el_item.get_element('view.film-schedule-info>view.schedule-select')
                    break

            return el_checkbox

        @property
        def total_of_schedule(self):
            """确认按钮上显示选择的天和排期总计"""

            selector = 'view.cart-bottom>view.cinema-bottom>view'
            el_views = self.page.get_elements(selector)
            el_total = None
            for el_view in el_views:
                if self.page.get_total_of_schedule(el_view.inner_text) is not None:
                    el_total = el_view
                    break
            return el_total

        @property
        def confirm_btn(self):
            """确认按钮"""

            inner_text = '确认'
            selector = 'view.cart-bottom>view.cinema-bottom>view'
            return self.page.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def cinema_name_equals(self, name):
            """影院详情页显示的影院名称是否等于预期

            Args:
                name: 预期影院名称
            """

            a_name = self.page.elements.cinema_name.inner_text
            if a_name != name:
                self.page.fail('影院详情页显示的影院名称({})不等于预期({})'.format(a_name, name))
            return self

        def cinema_address_equals(self, address):
            """影院详情页显示的影院地址是否等于预期"""

            addr = self.page.elements.cinema_address.inner_text
            if addr.strip() != address.strip():
                self.page.fail('影院详情页显示的影院地址({})不等于预期({})'.format(addr, address))
            return self

        def click_all_films(self):
            """点击 影片全选复选框"""

            self.page.elements.select_all_film_checkbox.click()
            return self

        def click_film(self, film_name, checked=True):
            """点击 影片复选框

            Args:
                film_name: 影片名称
                checked: True --- 选中  False --- 不选中
            """
            checked_image = '/images/checked.png'
            checkbox, image = self.page.elements.film_checkbox(film_name)
            src = ''.join(image.attribute('src'))
            print('src==', src)
            if checked:
                if src != checked_image:
                    checkbox.click()
            else:
                if src == checked_image:
                    checkbox.click()
            return self

        def select_day(self, day):
            """选择 日期"""

            self.page.elements.cinema_day(day).click()
            return self

        def click_all_schedule(self):
            """点击 全选当日排期复选框"""

            self.page.elements.select_all_schedule_checkbox.click()
            return self

        def click_schedule(self, film_name, hall_name, showtime):
            """点击 排期复选框

            Args:
                film_name: 影片名称
                hall_name: 影厅名称
                showtime: 放映开始时间
            """

            self.page.elements.film_schedule_checkbox(film_name, hall_name, showtime).click()
            return self

        def check_total_of_schedule(self, td, ts):
            """检查确认按钮上显示选择的天和排期总计

            Args:
                td: 天数
                ts: 排期场数
            """

            text = self.page.elements.total_of_schedule.inner_text
            result = self.page.get_total_of_schedule(text)
            if result is None:
                self.page.fail('确认按钮上显示选择的天和排期总计(共选中 天， 场排期)不等于预期(共选中{}天，{}场排期)'.format(td, ts))
            a_td, a_ts = result
            error_msg = []
            if int(a_td) != int(td):
                error_msg.append('确认按钮上显示的天数({})不等于预期天数({})'.format(a_td, td))
            if int(a_ts) != int(ts):
                error_msg.append('确认按钮上显示的排期场数({})不等于预期排期场数({})'.format(a_ts, ts))

            if len(error_msg) > 0:
                self.page.fail('; '.join(error_msg))
            return self

        def confirm(self):
            """点击 确认按钮"""

            self.page.elements.confirm_btn.click()
            return self
