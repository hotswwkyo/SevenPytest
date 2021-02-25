# -*- coding: utf-8 -*-
import re
from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class ADPlaceManagePage(BasePage):
    """广告位管理页面"""
    def get_limit_number(self, limit_text_of_per_page):
        """获取每页显示条数"""

        regex = '^(\\d+).*'
        pattern = re.compile(regex)
        matcher = pattern.search(limit_text_of_per_page)
        if matcher:
            return matcher.group(1)
        else:
            return None

    def get_total_datas(self, total_data_text):
        """获取数据总数"""

        regex = '\\d+-\\d+\\s共(\\d+)条$'
        pattern = re.compile(regex)
        matcher = pattern.search(total_data_text)
        if matcher:
            return matcher.group(1)
        else:
            return None

    class Elements(BasePage.Elements):
        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def film_name(self):
            """影片名称输入框"""

            label = '影片名称'
            return self._search_form_input(label)

        @property
        def cinema_name(self):
            """影院名称输入框"""

            label = '影院名称'
            return self._search_form_input(label)

        @property
        def belong_area(self):
            """所在地区输入框"""

            label = '所在地区'
            return self._search_form_input(label)

        def _search_form_button(self, name):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//span[contains(@class,"table-page-search-submitButtons")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def search_btn(self):
            """查询按钮"""

            return self._search_form_button('查 询')

        @property
        def reset_btn(self):
            """重置按钮"""

            return self._search_form_button('重 置')

        def _table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    ad_place_number: 广告位编号
                    belong_area: 所属地区
                    cinema_name: 影院名称
                    cinema_type: 影厅类型
                    film_name: 影片名称
                    showtime: 排期时间
                    duration: 签约时长
                    rest: 剩余时长
            """
            ad_place_number_index = 2
            belong_area_index = 3
            cinema_name_index = 4
            cinema_type_index = 5
            film_name_index = 6
            showtime_index = 7
            duration_index = 8
            rest_index = 9

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/tbody/tr/'

            btn_col = 'td/div/button/span[normalize-space()="{name}"]'.format(name=name)
            ad_place_number_col = 'td[position()={index} and normalize-space()="{ad_place_number}"]'
            belong_area_col = 'td[position()={index} and normalize-space()="{belong_area}"]'
            cinema_name_col = 'td[position()={index} and normalize-space()="{cinema_name}"]'
            cinema_type_col = 'td[position()={index} and normalize-space()="{cinema_type}"]'
            film_name_col = 'td[position()={index} and normalize-space()="{film_name}"]'
            showtime_col = 'td[position()={index} and normalize-space()="{showtime}"]'
            duration_col = 'td[position()={index} and normalize-space()="{duration}"]'
            rest_col = 'td[position()={index} and normalize-space()="{rest}"]'
            this_row = '/ancestor::tr[@data-row-key]'

            ad_place_number_k = 'ad_place_number'
            belong_area_k = 'belong_area'
            cinema_name_k = 'cinema_name'
            cinema_type_k = 'cinema_type'
            film_name_k = 'film_name'
            showtime_k = 'showtime'
            duration_k = 'duration'
            rest_k = 'rest'

            valid_keys = [ad_place_number_k, cinema_name_k, belong_area_k, cinema_type_k, film_name_k, showtime_k, duration_k, rest_k]

            has_vaild_key = False
            for k in valid_keys:
                if k in rowinfo.keys():
                    has_vaild_key = True
                    break
            if not has_vaild_key:
                raise KeyError('没有以下任意键：' + ", ".join(valid_keys))
            cols = []
            if ad_place_number_k in rowinfo:
                cxpath = ad_place_number_col.format(index=ad_place_number_index, ad_place_number=rowinfo[ad_place_number_k])
                cols.append(cxpath)

            if cinema_name_k in rowinfo:
                cxpath = cinema_name_col.format(index=cinema_name_index, cinema_name=rowinfo[cinema_name_k])
                cols.append(cxpath)

            if belong_area_k in rowinfo:
                cxpath = belong_area_col.format(index=belong_area_index, belong_area=rowinfo[belong_area_k])
                cols.append(cxpath)

            if cinema_type_k in rowinfo:
                cxpath = cinema_type_col.format(index=cinema_type_index, cinema_type=rowinfo[cinema_type_k])
                cols.append(cxpath)

            if film_name_k in rowinfo:
                cxpath = film_name_col.format(index=film_name_index, film_name=rowinfo[film_name_k])
                cols.append(cxpath)

            if showtime_k in rowinfo:
                cxpath = showtime_col.format(index=showtime_index, showtime=rowinfo[showtime_k])
                cols.append(cxpath)

            if duration_k in rowinfo:
                cxpath = duration_col.format(index=duration_index, duration=rowinfo[duration_k])
                cols.append(cxpath)

            if rest_k in rowinfo:
                cxpath = rest_col.format(index=rest_index, rest=rowinfo[rest_k])
                cols.append(cxpath)

            cols.append(btn_col)
            xpath_body = "/parent::tr/".join(cols)
            full_xpath = xpath_header + xpath_body
            row_xpath = full_xpath + this_row
            el_tr = self.page.find_element_by_xpath(row_xpath)
            drk = el_tr.get_attribute('data-row-key')
            ant_table_scroll_div = '/ancestor::div[contains(@class,"ant-table-scroll")]/following-sibling::div//table/tbody/tr[@data-row-key="{drk}"]/td/div/button/span[normalize-space()="{name}"]/parent::*'.format(
                drk=drk, name=name)
            xpath = row_xpath + ant_table_scroll_div
            return self.page.find_element_by_xpath(xpath)

        def see_btn(self, rowinfo):
            """查看按钮"""

            name = "查 看"
            return self._table_row_button(name, rowinfo)

        @property
        def _paging_toolbar_xpath(self):
            """ 分页工具栏 """

            header_row_titles = [
                'th[@key]/div[normalize-space()="{text}"]'.format(text="广告位编号"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="所在地区"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="影院名称"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="影厅类型"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="影片名称"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="排期时间"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="签约时长"),
                'th[@key]/div[normalize-space()="{text}"]'.format(text="剩余时长"),
            ]

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]//div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-scroll")]/div/table/thead/tr/'

            sibling_div = '/ancestor::table/ancestor::div[contains(@class,"ant-table-scroll")]/parent::div[contains(@class,"ant-table-content")]/parent::div[contains(@class,"ant-table")]/following-sibling::ul[contains(@class,"ant-pagination")]'

            xpath_body = "/ancestor::tr/".join(header_row_titles)
            full_xpath = xpath_header + xpath_body
            xpath = full_xpath + sibling_div
            return xpath

        @property
        def total(self):
            """页面显示的总条数"""

            p = '上一页'
            n = '下一页'
            rest_xpath = '/li[@title="{p}"]/parent::ul/li[@title="{n}"]/parent::ul/li[contains(@class,"ant-pagination-total-text")]'.format(p=p, n=n)
            xpath = self._paging_toolbar_xpath + rest_xpath
            return self.page.find_element_by_xpath(xpath)

        @property
        def limit_of_per_page(self):
            """每页显示的条数"""

            p = '上一页'
            n = '下一页'
            rest_xpath = '/li[@title="{p}"]/parent::ul/li[@title="{n}"]/parent::ul/li[contains(@class,"ant-pagination-options")]/div/div/div/div'.format(p=p, n=n)
            xpath = self._paging_toolbar_xpath + rest_xpath
            return self.page.find_element_by_xpath(xpath)

        @property
        def jump_to_page_inputbox(self):
            """每页显示的条数"""

            p = '上一页'
            n = '下一页'
            jump_text = '跳至'
            rest_xpath = '/li[@title="{p}"]/parent::ul/li[@title="{n}"]/parent::ul/li[contains(@class,"ant-pagination-options")]/div[contains(@class,"ant-pagination-options-quick-jumper") and contains(text(),"{jump_text}")]/input'.format(
                p=p, n=n, jump_text=jump_text)
            xpath = self._paging_toolbar_xpath + rest_xpath
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def film_name(self, code):
            """输入影片名称"""

            self.page.elements.film_name.clear()
            self.page.elements.film_name.send_keys(code)
            return self

        def cinema_name(self, name):
            """输入影院名称"""

            self.page.elements.cinema_name.clear()
            self.page.elements.cinema_name.send_keys(name)
            return self

        def belong_area(self, name):
            """输入所在地区"""

            self.page.elements.belong_area.clear()
            self.page.elements.belong_area.send_keys(name)
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def see(self, rowinfo):
            """点击 查看按钮

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    ad_place_number: 广告位编号
                    belong_area: 所属地区
                    cinema_name: 影院名称
                    cinema_type: 影厅类型
                    film_name: 影片名称
                    showtime: 排期时间
                    duration: 签约时长
                    rest: 剩余时长
            """

            self.page.elements.see_btn(rowinfo).click()
            return self

        def turn_to_page(self, page_number):

            self.page.elements.jump_to_page_inputbox.clear()
            self.page.elements.jump_to_page_inputbox.send_keys(page_number)
            return self
