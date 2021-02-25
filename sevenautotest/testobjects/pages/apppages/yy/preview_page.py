# -*- coding: utf-8 -*-
from sevenautotest.utils.winspy import WindowSpy as spy
from sevenautotest.basepage.base_minium_page import BaseMiniumPage

__author__ = "si wen wei"


class PreviewPage(BaseMiniumPage):
    """预览页面"""
    class Elements(BaseMiniumPage.Elements):
        @property
        def edit_btn(self):
            """编辑 按钮"""

            inner_text = '编辑'
            selector = 'view.swiper-box>view>view.operation>view.operation-btn'
            el_swiper = self.page.get_element('view.page').get_element('swiper')
            el_preview = el_swiper.get_element('swiper-item>preview#release')
            el_preview.click()
            self.page.sleep(1)
            el_btn = el_preview.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def release_btn(self):
            """发布 按钮"""

            inner_text = '发布'
            selector = 'view.swiper-box>view>view.operation>view.operation-btn'
            el_swiper = self.page.get_element('view.page').get_element('swiper')
            el_preview = el_swiper.get_element('swiper-item>preview#release')
            el_preview.click()
            self.page.sleep(1)
            el_btn = el_preview.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def title_inputbox(self):
            """广告标题 输入框"""

            selector = 'view.swiper-box>view>view>view.controls-preview-input>input.weui-input'
            el_swiper = self.page.get_element('view.page').get_element('swiper')
            el_preview = el_swiper.get_element('swiper-item>preview#release')
            el_preview.click()
            self.page.sleep(1)
            el_input = el_preview.get_element(selector)
            return el_input

    class Actions(BaseMiniumPage.Actions):
        def input_title(self, title):
            """输入标题"""

            self.page.elements.title_inputbox.trigger("input", {"value": title})
            return self

        def edit(self):
            """点击 编辑按钮"""

            self.page.elements.edit_btn.click()
            return self

        def release(self):
            """点击 发布按钮"""

            self.page.elements.release_btn.click()
            return self

        def confirm(self):

            spy.mouse_move(1668, 577)
            self.sleep(2)
            spy.mouse_click(1668, 577)
            return self
