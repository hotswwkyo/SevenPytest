# -*- coding: utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage

__author__ = "si wen wei"


class ClipPage(BaseMiniumPage):
    """剪辑页面"""
    class Elements(BaseMiniumPage.Elements):
        @property
        def add_btn(self):
            """添加 按钮"""

            inner_text = '添加'
            selector = 'view.swiper-box>view>view.operation>view>text'
            el_swiper_item = self.page.get_element('view.page>swiper>swiper-item')
            el_videomy = el_swiper_item.get_element('videomy#video')
            el_videomy.click()
            self.page.sleep(1)
            el_btn = el_videomy.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def remove_btn(self):
            """删除 按钮"""

            inner_text = '删除'
            selector = 'view.swiper-box>view>view.operation>view>text'
            el_swiper_item = self.page.get_element('view.page>swiper>swiper-item')
            el_videomy = el_swiper_item.get_element('videomy#video')
            el_videomy.click()
            self.page.sleep(1)
            el_btn = el_videomy.get_element(selector, inner_text=inner_text)
            return el_btn

        @property
        def clip_btn(self):
            """剪辑 按钮"""

            selector = 'view>image'
            el_mp_tabbar = self.page.get_element('view.page>mp-tabbar')
            el_mp_tabbar.click()
            self.page.sleep(1)
            el_items = el_mp_tabbar.get_elements('view.weui-tabbar>view.weui-tabbar__item')
            el_btn = None
            for el_item in el_items:
                el_image = el_item.get_element(selector)
                if el_image:
                    src = el_image.attribute('src')
                    if "".join(src).endswith('images/video-clip-active.svg'):
                        el_btn = el_item
                        break
            return el_btn

        @property
        def video_music_btn(self):
            """配音乐 按钮"""

            selector = 'view>image'
            el_mp_tabbar = self.page.get_element('view.page>mp-tabbar')
            el_mp_tabbar.click()
            self.page.sleep(1)
            el_items = el_mp_tabbar.get_elements('view.weui-tabbar>view.weui-tabbar__item')
            el_btn = None
            for el_item in el_items:
                el_image = el_item.get_element(selector)
                if el_image:
                    src = el_image.attribute('src')
                    if "".join(src).endswith('images/video-music.svg'):
                        el_btn = el_item
                        break
            return el_btn

        @property
        def video_text_btn(self):
            """配字幕 按钮"""

            selector = 'view>image'
            el_mp_tabbar = self.page.get_element('view.page>mp-tabbar')
            el_mp_tabbar.click()
            self.page.sleep(1)
            el_items = el_mp_tabbar.get_elements('view.weui-tabbar>view.weui-tabbar__item')
            el_btn = None
            for el_item in el_items:
                el_image = el_item.get_element(selector)
                if el_image:
                    src = el_image.attribute('src')
                    if "".join(src).endswith('images/video-text.svg'):
                        el_btn = el_item
                        break
            return el_btn

        @property
        def preview_btn(self):
            """预览 按钮"""

            selector = 'view>image'
            el_mp_tabbar = self.page.get_element('view.page>mp-tabbar')
            el_mp_tabbar.click()
            self.page.sleep(1)
            el_items = el_mp_tabbar.get_elements('view.weui-tabbar>view.weui-tabbar__item')
            el_btn = None
            for el_item in el_items:
                el_image = el_item.get_element(selector)
                if el_image:
                    src = el_image.attribute('src')
                    if "".join(src).endswith('images/preview.svg'):
                        el_btn = el_item
                        break
            return el_btn

    class Actions(BaseMiniumPage.Actions):
        def add(self):
            """点击 添加按钮"""

            self.page.elements.add_btn.click()
            return self

        def remove(self):
            """点击 删除按钮"""

            self.page.elements.remove_btn.click()
            return self

        def clip(self):
            """点击 剪辑按钮"""

            self.page.elements.clip_btn.click()
            return self

        def video_music(self):
            """点击 配乐按钮"""

            self.page.elements.video_music_btn.click()
            return self

        def video_text(self):
            """点击 配字幕按钮"""

            self.page.elements.video_text_btn.click()
            return self

        def preview(self):
            """点击 预览按钮"""

            self.page.elements.preview_btn.click()
            return self
