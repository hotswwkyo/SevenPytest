# -*- coding:utf-8 -*-
from sevenautotest.utils.winspy import WindowSpy as spy
from sevenautotest.utils import helper
from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class IndexPage(BaseMiniumPage):
    """ 首页 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def form(self):
            """表单区域"""

            selector = '#form'
            return self.page.get_element(selector)

        @property
        def area(self):
            """投放地区："""

            selector = '.weui-select'
            inner_text = '投放地区：'
            return self.form.get_element('view').get_element(selector, inner_text=inner_text)

        def curr_area(self, area):
            """当前投放地区"""

            selector = 'text'
            inner_text = area
            el = self.form.get_element('view').get_element(selector, inner_text=inner_text)
            if not el:
                self.page.raise_error('找不到投放地区：{}'.format(area))
            return el

        @property
        def duration(self):
            """投放周期："""

            selector = '.weui-select'
            inner_text = '投放周期：'
            return self.form.get_element('view').get_element(selector, inner_text=inner_text)

        def curr_duration(self, duration):
            """当前投放周期"""

            selector = 'text'
            inner_text = duration
            el = self.form.get_element('view').get_element(selector, inner_text=inner_text)
            if not el:
                self.page.raise_error('找不到投放周期：{}'.format(duration))
            return el

        @property
        def cinema_ad_btn(self):
            """投放影院广告"""

            selector = 'button'
            inner_text = '投放影院广告'
            return self.form.get_element('view').get_element('view.search-btn').get_element(selector, inner_text=inner_text)

        @property
        def make_ad_btn(self):
            """制作广告片"""

            selector = 'button'
            inner_text = '制作广告片'
            return self.form.get_element('view').get_element('view.search-btn').get_element(selector, inner_text=inner_text)

        @property
        def notice_dialog_close_btn(self):
            """新手须知弹窗关闭按钮"""

            selector = 'mp-icon'
            el_dialog = self.page.get_element('view>cs-dialog')
            el_dialog.click()
            self.page.sleep(1)
            el_hview = el_dialog.get_element('view').get_element('view').get_element('view').get_element('view').get_element('view.notice-header')
            el_btn = el_hview.get_element(selector)
            return el_btn

        @property
        def upload_option_win_title(self):
            """上传选项窗口标题"""

            selector = 'view.weui-actionsheet>view.weui-actionsheet__title>view.weui-actionsheet__title-text'
            el_mp_as = self.page.get_element('view>mp-actionsheet')
            el_mp_as.click()
            self.page.sleep(1)
            el_title = el_mp_as.get_element(selector)
            return el_title

        @property
        def select_upload_picture_btn(self):
            """选择图片 按钮"""

            inner_text = '选择图片'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__menu>view.weui-actionsheet__cell'

            el_mp_as = self.page.get_element('view>mp-actionsheet')
            el_mp_as.click()
            self.page.sleep(1)
            el_btn = el_mp_as.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def select_upload_video_btn(self):
            """选择视频 按钮"""

            inner_text = '选择视频'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__menu>view.weui-actionsheet__cell'

            el_mp_as = self.page.get_element('view>mp-actionsheet')
            el_mp_as.click()
            self.page.sleep(1)
            el_btn = el_mp_as.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def cancel_btn(self):
            """取消 按钮"""

            inner_text = '取消'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__action>view.weui-actionsheet__cell'

            el_mp_as = self.page.get_element('view>mp-actionsheet')
            el_mp_as.click()
            self.page.sleep(1)
            el_btn = el_mp_as.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def tabbar(self):
            """首页下方tab工具栏"""

            selector = '.mp-tabbar'
            el = self.page.get_element(selector)
            el.click()
            self.page.sleep(2)
            return el

        @property
        def home_tab(self):
            """首页 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "首页"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def ad_tab(self):
            """广告篮 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "广告篮"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def order_tab(self):
            """订单 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "订单"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def my_tab(self):
            """我的 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "我的"
            return self.tabbar.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def click_form(self):

            self.page.elements.form.click()
            return self

        def click_tabbar(self):
            """点击下方标签工具栏"""

            self.page.elements.tabbar.click()
            return self

        def click_home_tab(self):
            """点击下方首页标签"""

            self.page.elements.home_tab.click()
            return self

        def click_ad_tab(self):
            """点击下方广告篮标签"""

            self.page.elements.ad_tab.click()
            return self

        def click_order_tab(self):
            """点击下方订单标签"""

            self.page.elements.order_tab.click()
            return self

        def click_my_tab(self):

            self.page.elements.my_tab.click()
            return self

        def click_area(self):
            """点击下方我的标签"""

            self.page.elements.area.click()
            return self

        def click_duration(self):
            """ 点击投放周期 """
            self.page.elements.duration.click()
            return self

        def find_curr_area(self, area_text):

            ca = self.page.elements.curr_area(area_text)
            outer_wxml = ca.outer_wxml
            helper.ignore_unused(outer_wxml)
            return self

        def find_curr_duration(self, duration):

            cd = self.page.elements.curr_duration(duration)
            helper.ignore_unused(cd)
            return self

        def click_cinema_ad_btn(self):
            """点击 投放影院广告"""

            self.page.elements.cinema_ad_btn.click()
            return self

        def click_make_ad_btn(self):
            """点击 制作广告片"""

            self.page.elements.make_ad_btn.click()
            return self

        def click_notice_dialog_close_btn(self, which_btn='ad'):
            """点击 新手须知 弹窗的关闭按钮

            Args:
                which: 关闭新手须知对话框后 点击哪个按钮 cinema - [投放影院广告]按钮   ad - [制作广告片]按钮

            """

            btn = self.page.elements.notice_dialog_close_btn
            if btn:
                btn.tap()
                self.sleep(1)
                if which_btn.lower() == 'ad'.lower():
                    self.click_make_ad_btn()
                else:
                    self.click_cinema_ad_btn()
            return self

        def click_select_upload_picture_btn(self):
            """点击 选择图片 按钮"""

            self.page.elements.select_upload_picture_btn.click()
            return self

        def input_upload_picture_path(self, filepath):

            win_title = '打开'
            exist = spy.win_wait(win_title)
            if exist:
                spy.win_activate(win_title)
                spy.control_set_text(win_title, 'Edit1', filepath)
                self.sleep(1)
                spy.control_click(win_title, "Button1", text='打开(&O)')
            else:
                self.page.raise_error('找不到选择上传图片窗口')
            return self

        def click_select_upload_video_btn(self):
            """点击 选择视频 按钮"""

            self.page.elements.select_upload_video_btn.click()
            return self

        def input_upload_video_path(self, filepath):

            win_title = '打开'
            exist = spy.win_wait(win_title)
            if exist:
                spy.win_activate(win_title)
                spy.control_set_text(win_title, 'Edit1', filepath)
                self.sleep(1)
                spy.control_click(win_title, "Button1", text='打开(&O)')
            else:
                self.page.raise_error('找不到选择上传视频窗口')
            return self

        def upload_option_win_title_equals(self, title):
            """检查上传选项窗口标题"""

            atitle = self.page.elements.upload_option_win_title.inner_text
            if atitle != title:
                self.page.fail('{} != {}'.format(atitle, title))
            return self

        def cancel(self):

            self.page.elements.cancel_btn.click()
            return self
