# -*- coding:utf-8 -*-
import re
from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class CinemaListPage(BaseMiniumPage):
    """影院列表页面"""
    def get_total_of_selected_cinemas(self, total_data_text):
        """获取已选择影院总数"""

        regex = '已选(\\d+)家影院$'
        pattern = re.compile(regex)
        matcher = pattern.search(total_data_text)
        if matcher:
            return matcher.group(1)
        else:
            return None

    class Elements(BaseMiniumPage.Elements):
        @property
        def page_title(self):

            inner_text = '影院列表'
            selector = 'view.navigation>mp-navigation-bar'
            el_topbar = self.page.get_element(selector)
            el_topbar.click()
            self.page.sleep(1)
            return el_topbar.get_element('text', inner_text=inner_text)

        @property
        def upload_ad_btn(self):
            """去上传广告片"""

            selector = 'view.fixed-bottom'
            inner_text = '去上传广告片'
            el_y = self.page.get_element(selector).get_element('view.go-ad', inner_text=inner_text)
            return el_y

        def ad_name(self, name):
            """广告片名称"""

            selector = 'view.container>view.cinema-list>view>view.flex-row-video>view.row-video-left>text'
            el_name = self.page.get_element(selector, inner_text=name)
            return el_name

        def ad_duration(self, duration):
            """广告片时长"""

            selector = 'view.container>view.cinema-list>view>view.flex-row-video>view.row-video-right>text'
            el_name = self.page.get_element(selector, inner_text=duration)
            return el_name

        @property
        def change_btn(self):
            """更换按钮"""

            inner_text = '更换'
            selector = 'view.container>view.cinema-list>view>view.flex-row-video>view.row-video-right>text'
            el_btn = self.page.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def area_btn(self):
            """地区按钮"""

            inner_text = '地区'
            selector = 'view.container>view.cinema-list>view>view.search-info>view.search-item.search-info-area>text'
            el_btn = self.page.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def time_btn(self):
            """周期按钮"""

            inner_text = '周期'
            selector = 'view.container>view.cinema-list>view>view.search-info>view.search-item.search-info-time>text'
            el_btn = self.page.get_element(selector, inner_text=inner_text)
            return el_btn

        def cinema_checkbox(self, cinema_name):
            """影院复选框"""

            inner_text = cinema_name
            selector = 'view.container>view.cinema-list>view.cart-contaner>view.cart-box>view.cart-goods'
            el_goods = self.page.get_elements(selector)
            el_btn = None
            for el_good in el_goods:
                el_text = el_good.get_element('view>view>view.cinema-name>text', inner_text=inner_text)
                if el_text:
                    el_btn = el_good.get_element('view>image')
                    if el_btn:
                        break
            return el_btn

        def cinema_item(self, cinema_name):
            """影院详情按钮"""

            inner_text = cinema_name
            goods_selector = 'view.container>view.cinema-list>view.cart-contaner>view.cart-box>view.cart-goods'
            cinema_selector = 'view>view>view.cinema-name>text'
            selector = '{}>{}'.format(goods_selector, cinema_selector)
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def total_of_shopping_basket(self):
            """广告篮显示数字的元素"""

            selector = 'view.weui-badge'
            el_fb_view = self.page.get_element('view.container>view.fixed-bottom.cart-bottom-ad')
            el_mp_badge = el_fb_view.get_element('view.cart-bottom-ad-left>view>mp-badge')
            el_mp_badge.click()
            self.page.sleep(1)
            el_total = el_mp_badge.get_element(selector)
            return el_total

        @property
        def shopping_basket(self):
            """广告篮按钮"""

            selector = 'view.cart-bottom-ad-left>view>image'
            el_fb_view = self.page.get_element('view.container>view.fixed-bottom.cart-bottom-ad')
            el_basket = el_fb_view.get_element(selector)
            return el_basket

        @property
        def total_selected_cinema(self):
            """加入广告篮上方显示的已选择影院总数"""

            selector = 'view>button>text'
            el_fb_view = self.page.get_element('view.container>view.fixed-bottom.cart-bottom-ad')
            el_texts = el_fb_view.get_elements(selector)
            el_show_total = None
            for el_text in el_texts:
                inner_text = el_text.inner_text
                if self.page.get_total_of_selected_cinemas(inner_text) is not None:
                    el_show_total = el_text
                    break
            return el_show_total

        @property
        def join_to_ad_basket_btn(self):
            """加入广告篮按钮"""

            selector = 'view>button>text'
            inner_text = '加入广告篮'
            el_fb_view = self.page.get_element('view.container>view.fixed-bottom.cart-bottom-ad')
            el_btn = el_fb_view.get_element(selector, inner_text=inner_text)
            return el_btn

    class Actions(BaseMiniumPage.Actions):
        def upload_ad(self):
            """点击 去上传广告片"""

            self.page.elements.upload_ad_btn.click()
            return self

        def find_ad_name(self, name):
            """ 查找当前选中的广告名称 """

            el_name = self.page.elements.ad_name(name)
            if not el_name:
                self.page.fail('找不到广告：{}'.format(name))
            return self

        def find_ad_duration(self, duration):
            """ 查找当前选中的广告时长 """

            if not self.page.elements.ad_duration(duration):
                self.page.fail('找不到时长({})的广告'.format(duration))
            return self

        def change(self):
            """ 点击更换按钮 """

            self.page.elements.change_btn.click()
            return self

        def check_total_of_shopping_basket(self, total):
            """ 检查广告篮显示的总数是否正确 """

            inner_text = self.page.elements.total_of_shopping_basket.inner_text
            a_total = int(inner_text.strip())
            e_total = int(total)
            if a_total != e_total:
                self.page.fail('广告篮中显示的总数({})与预期({})不等'.format(a_total, e_total))
            return self

        def shopping_basket(self):
            """ 点击 广告篮按钮 """

            self.page.elements.shopping_basket.click()
            return self

        def check_total_selected_cinema(self, total):
            """ 检查加入广告篮上方显示的已选择影院总数 """

            inner_text = self.page.elements.total_selected_cinema.inner_text
            number_str = self.page.get_total_of_selected_cinemas(inner_text)
            e_total = int(total)
            if number_str is None:
                self.page.fail('检查加入广告篮上方显示的已选择影院总数()与预期({})不相等'.format(e_total))
            else:
                a_total = int(number_str)
                if a_total != e_total:
                    self.page.fail('检查加入广告篮上方显示的已选择影院总数({})与预期({})不相等'.format(a_total, e_total))
            return self

        def join_to_ad_basket(self):
            """ 点击 加入广告篮按钮 """

            self.page.elements.join_to_ad_basket_btn.click()
            return self

        def click_area(self):
            """ 点击 地区按钮"""

            self.page.elements.area_btn.click()
            return self

        def click_time(self):
            """ 点击 周期按钮"""

            self.page.elements.time_btn.click()
            return self

        def click_cinema_checkbox(self, name):
            """ 点击影院复选框 """

            self.page.elements.cinema_checkbox(name).click()
            return self

        def click_cinema_item(self, name):
            """ 点击影院详情按钮 """

            self.page.elements.cinema_item(name).click()
            return self

        def is_page_self(self, path=None, failmsg="找不到影院列表页面"):

            page_title = self.page.elements.page_title
            cpp = self.page.current_page.path
            if path and cpp != path:
                self.page.fail(failmsg + '：页面路径({}) != 预期({})'.format(cpp, path))
            if not page_title:
                self.page.fail(failmsg)
            return self
