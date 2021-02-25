# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class MyAdListPage(BaseMiniumPage):
    """ 我的广告素材页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def page_title(self):
            """页面标题"""

            selector = 'mp-navigation-bar'
            inner_text = '我的广告素材'
            el_bar = self.page.get_element(selector)
            el_bar.click()
            self.page.sleep(1)
            return self.page.get_element('text', inner_text=inner_text)

        def ad_checkbox(self, name):
            """广告素材 复选框"""

            selector = 'view.content>view.text>view.title'
            el_svs = self.page.get_elements('view.weui-cells>mp-slideview')
            el_checkbox = None
            for i, el_sv in enumerate(el_svs):
                el_sv.click()
                self.page.sleep(1)
                el_mpcell = el_sv.get_element('view>view>mp-cell')
                el_mpcell.click()
                self.page.sleep(1)
                el_scell = el_mpcell.get_element('view').get_element('view.weui-cell__bd').get_element('view.weui-slidecell')
                el_name = el_scell.get_element(selector, inner_text=name)
                if el_name:
                    el_checkbox = el_scell.get_element('view.image-active')
                    break
                if i + 1 >= len(el_svs):
                    self.page.fail('我的广告素材找不到广告：{}'.format(name))
            return el_checkbox

        def ad_duration(self, name):
            """广告素材 时长"""

            selector = 'view.content>view.text>view.title'
            el_svs = self.page.get_elements('view.weui-cells>mp-slideview')
            el_d = None
            for i, el_sv in enumerate(el_svs):
                el_sv.click()
                self.page.sleep(1)
                el_mpcell = el_sv.get_element('view>view>mp-cell')
                el_mpcell.click()
                self.page.sleep(1)
                el_scell = el_mpcell.get_element('view').get_element('view.weui-cell__bd').get_element('view.weui-slidecell')
                el_name = el_scell.get_element(selector, inner_text=name)
                if el_name:
                    el_d = el_scell.get_element('view.content>view.text>view.sub-title>text.m')
                    break
                if i + 1 >= len(el_svs):
                    self.page.fail('我的广告素材找不到广告：{}'.format(name))
            return el_d

        def ad_showdate(self, name):
            """广告素材 日期"""

            selector = 'view.content>view.text>view.title'
            el_svs = self.page.get_elements('view.weui-cells>mp-slideview')
            el_showdate = None
            for i, el_sv in enumerate(el_svs):
                el_sv.click()
                self.page.sleep(1)
                el_mpcell = el_sv.get_element('view>view>mp-cell')
                el_mpcell.click()
                self.page.sleep(1)
                el_scell = el_mpcell.get_element('view').get_element('view.weui-cell__bd').get_element('view.weui-slidecell')
                el_name = el_scell.get_element(selector, inner_text=name)
                if el_name:
                    el_showdate = el_scell.get_element('view.content>view.text>view.sub-title>text.time')
                    break
                if i + 1 >= len(el_svs):
                    self.page.fail('我的广告素材找不到广告：{}'.format(name))
            return el_showdate

        def del_btn(self, name):
            """广告素材 删除按钮"""

            selector = 'view.content>view.text>view.title'
            el_svs = self.page.get_elements('view.weui-cells>mp-slideview')
            el_btn = None
            for i, el_sv in enumerate(el_svs):
                el_sv.click()
                self.page.sleep(1)
                el_mpcell = el_sv.get_element('view>view>mp-cell')
                el_mpcell.click()
                self.page.sleep(1)
                el_scell = el_mpcell.get_element('view').get_element('view.weui-cell__bd').get_element('view.weui-slidecell')
                el_name = el_scell.get_element(selector, inner_text=name)
                if el_name:
                    el_btn = el_scell.get_element('view.content>view.footer>text', inner_text='删除')
                    break
                if i + 1 >= len(el_svs):
                    self.page.fail('我的广告素材找不到广告：{}'.format(name))
            return el_btn

        @property
        def to_make_btn(self):
            """去制作按钮"""

            inner_text = '去制作'
            selector = 'view.buttons>navigator'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def to_launch_btn(self):
            """去投放按钮"""

            inner_text = '去投放'
            selector = 'view.buttons>navigator'
            return self.page.get_element(selector, inner_text=inner_text)

        @property
        def video_btn(self):
            """选择视频 按钮"""

            inner_text = '选择视频'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__menu>view'
            el_mp = self.page.get_element('mp-actionsheet')
            el_mp.click()
            self.page.sleep(1)
            return el_mp.get_element(selector, inner_text=inner_text)

        @property
        def picture_btn(self):
            """选择图片 按钮"""

            inner_text = '选择图片'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__menu>view'
            el_mp = self.page.get_element('mp-actionsheet')
            el_mp.click()
            self.page.sleep(1)
            return el_mp.get_element(selector, inner_text=inner_text)

        @property
        def cancel_btn(self):
            """取消 按钮"""

            inner_text = '取消'
            selector = 'view.weui-actionsheet>view.weui-actionsheet__action>view'
            el_mp = self.page.get_element('mp-actionsheet')
            el_mp.click()
            self.page.sleep(1)
            return el_mp.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def check_ad_is_exists(self, name, pass_if_exists=True, failmsg=""):
            """检查广告素材是否存在

            Args:
                name: 广告素材名称
                pass_if_exists:
            """

            el = self.page.elements.ad_checkbox(name)
            if pass_if_exists:
                if not el:
                    self.page.fail("找不到广告素材：{}".format(name) if not failmsg else failmsg)
            else:
                if el:
                    self.page.fail("广告素材({})存在".format(name) if not failmsg else failmsg)
            return self

        def click_ad_checkbox(self, name):
            """ 点击广告素材复选框

            Args:
                name: 广告名称
            """

            self.page.elements.ad_checkbox(name).click()
            return self

        def remove(self, name):
            """点击广告素材删除按钮"""

            self.page.elements.del_btn(name).click()
            return self

        def duration_equals(self, name, duration):
            """检查时长

            Args:
                name: 广告名称
                duration: 时长
            """

            a_duration = self.page.elements.ad_duration(name).inner_text
            if a_duration != duration:
                msg = '显示的广告{}时长({})与预期({})不等'.format(name, a_duration, duration)
                self.page.fail(msg)
            return self

        def showdate_equals(self, name, showdate):
            """检查日期

            Args:
                name: 广告名称
                showdate: 日期
            """

            a_showdate = self.page.elements.ad_showdate(name).inner_text
            if a_showdate != showdate:
                msg = '显示的广告{}日期({})与预期({})不等'.format(name, a_showdate, showdate)
                self.page.fail(msg)
            return self

        def to_make(self):
            """点击 去制作按钮"""

            self.page.elements.to_make_btn.click()
            return self

        def to_launch(self):
            """点击 去投放按钮"""

            self.page.elements.to_launch_btn.click()
            return self

        def click_video_btn(self):
            """点击 选择视频"""

            self.page.elements.video_btn.click()
            return self

        def click_picture_btn(self):
            """点击 选择图片"""

            self.page.elements.picture_btn.click()
            return self

        def cancel(self):

            self.page.elements.cancel_btn.click()
            return self

        def confirm_delete(self, x=1664, y=833):

            return self.click_xy(x, y)

        def is_page_self(self, failmsg="找不到我的广告素材页面"):

            page_title = self.page.elements.page_title
            if not page_title:
                self.page.fail(failmsg)
            return self
