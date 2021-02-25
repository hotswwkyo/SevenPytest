# -*- coding:utf-8 -*-
from sevenautotest.utils import helper
from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class AreaPage(BaseMiniumPage):
    """投放地区选择页面"""
    class Elements(BaseMiniumPage.Elements):
        def city(self, name):
            """省市"""

            selector = 'view.slide'
            inner_text = name
            return self.page.get_element(selector).get_element('scroll-view.left-slide').get_element('text', inner_text=inner_text)

        def area(self, name):
            """地区"""

            selector = 'view.slide'
            inner_text = name
            return self.page.get_element(selector).get_element('scroll-view.right-slide').get_element('text', inner_text=inner_text)

        @property
        def all_area(self):
            """全部地区"""

            return self.area('全部地区')

        def selected_area(self, name):
            """已经选中的地区，返回地区元素的关闭图标对象"""

            selector = 'view.footer'
            inner_text = name
            selected_city_views = self.page.get_element(selector).get_element('scroll-view.selected').get_element('view').get_elements('view.rows')
            parent = None
            for scv in selected_city_views:
                el_city = scv.get_element('text.select', inner_text=inner_text)
                if el_city and el_city.inner_text == inner_text:
                    # find element
                    parent = scv
                    break
            del_icon = parent.get_element('mp-icon')
            outer_wxml = del_icon.outer_wxml
            helper.ignore_unused(outer_wxml)
            return del_icon

        @property
        def all_selected_areas(self):
            """所有被选中的地区"""

            selector = 'view.footer'
            el_scroll = self.page.get_element(selector).get_element('scroll-view.selected')
            el_areas = el_scroll.get_elements('view>view.rows>text.select')
            return el_areas

        @property
        def clear_btn(self):
            """清空按钮"""

            selector = 'view.footer'
            inner_text = '清空'
            btn = self.page.get_element(selector).get_element('view.buttons').get_element('text.clear', inner_text=inner_text)
            outer_wxml = btn.outer_wxml
            helper.ignore_unused(outer_wxml)
            return btn

        @property
        def confirm_btn(self):
            """确认按钮"""

            selector = 'view.footer'
            inner_text = '确认'
            btn = self.page.get_element(selector).get_element('view.buttons').get_element('view.button').get_element('text', inner_text=inner_text)
            outer_wxml = btn.outer_wxml
            helper.ignore_unused(outer_wxml)
            return btn

    class Actions(BaseMiniumPage.Actions):
        def select_all(self):
            """点击 全部地区"""

            self.page.elements.all_area.click()
            return self

        def click_city(self, name):

            self.page.elements.city(name).click()
            return self

        def click_area(self, name):

            self.page.elements.area(name).click()
            return self

        def remove_selected_area(self, name):

            self.page.elements.selected_area(name).click()
            return self

        def clear(self):

            self.page.elements.clear_btn.click()
            return self

        def confirm(self):

            self.page.elements.confirm_btn.click()
            return self

        def check_area_is_selected(self, areas):
            """检查地区是否在选中列表中"""

            unselected = []
            el_areas = self.page.elements.all_selected_areas
            raw_areas = []
            unique_areas = []
            for el_area in el_areas:
                name = el_area.inner_text
                raw_areas.append(name)
                if name not in unique_areas:
                    unique_areas.append(name)
            a_selected_total = len(unique_areas)
            e_selected_total = len(areas)
            if a_selected_total != e_selected_total:
                self.page.fail('实际选中的地区({})与预期({})不等'.format(a_selected_total, e_selected_total))
            for area in areas:
                if area not in unique_areas:
                    unselected.append(area)
            if unselected:
                self.page.fail('以下地区未被选中：' + ', '.join(unselected))
            return self
