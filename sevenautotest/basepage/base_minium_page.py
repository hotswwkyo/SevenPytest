# -*- coding:utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from sevenautotest.utils import TestAssert
from sevenautotest.utils.winspy import WindowSpy as spy
from sevenautotest.basepage.abstract_base_minium_page import AbstractBaseMiniumPage


class BaseMiniumPage(AbstractBaseMiniumPage):
    """微信小程序根页面"""
    def init(self):

        pass

    def fail(self, message=""):

        TestAssert.fail(message)

    class Elements(AbstractBaseMiniumPage.Elements):
        pass

    class Actions(AbstractBaseMiniumPage.Actions):
        def input_upload_filepath(self, filepath):

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

        def click_xy(self, x, y):

            spy.mouse_move(x, y)
            self.sleep(2)
            spy.mouse_click(x, y)
            return self


if __name__ == "__main__":
    pass
