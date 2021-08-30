# -*- coding:utf-8 -*-

import io
import os
import base64
from PIL import ImageGrab
from sevenautotest import settings
from sevenautotest.utils.marker import ConstAttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager

__version__ = "1.0"
__author__ = "si wen wei"


class ScreenshotCapturer(AttributeManager):
    """优先使用浏览器截图，如果浏览器截图失败则执行整个屏幕截图"""

    SCREENSHOTS_DIR = ConstAttributeMarker(settings.SCREENSHOTS_DIR, "默认截图存放目录")

    def __init__(self, driver=None, screenshot_dir=None):
        """配置浏览器和截图存放目录

        @param driver WebDriver 实例 ，不设置则使用屏幕截图
        @param screenshot_dir 截图存放目录，不设置则使用默认目录
        """
        self.driver = driver
        self.set_screenshot_dir(screenshot_dir)

    def set_screenshot_dir(self, path=None):

        if path:
            path = os.path.abspath(path)
            self._create_directory(path)
        self.screenshot_root_directory = path
        return self

    @classmethod
    def screen_capture(cls, filename=None, region=None):
        """
        截屏返回PIL.Image对象

        Args:
         - filename: 保存截图文件的完整路径名，省略则不保存
         - region: 4整型数据构成的元祖 第1、2为起点坐标，第3、4位长宽，省略则截全屏

        Usage:
            ScreenshotCapturer.screen_capture('/screenshots/st.png')
        """

        im = ImageGrab.grab()
        if region is not None:
            assert len(region) == 4, 'region argument must be a tuple of four ints'
            region = [int(x) for x in region]
            im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))
        if filename is not None:
            im.save(filename)
        return im

    def _pil_screenshot(self, file_full_path):

        img = self.screen_capture()
        try:
            img.save(file_full_path, "png")
        except ValueError:
            return False
        except IOError:
            return False
        finally:
            del img
        return True

    def _browser_screenshot(self, file_full_path):

        try:
            return self.driver.get_screenshot_as_file(file_full_path)
        except Exception:
            return False

    def screenshot(self, filename):
        """浏览器截图失败则启用屏幕截图，返回结果和截图文件路径

        """

        result = False
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if self.driver:
            result = self._browser_screenshot(path)
        if not result:
            result = self._pil_screenshot(path)
        return (result, path)

    def screenshot_as_base64(self):

        try:
            if self.driver:
                return self.driver.get_screenshot_as_base64()
        except Exception as e:
            print(e)
        img = self.screen_capture()
        temp = io.BytesIO()
        try:
            img.save(temp, "png")
        except ValueError:
            pass
        except IOError:
            pass
        finally:
            del img
        img_datas = temp.getvalue()
        del temp
        return base64.b64encode(img_datas).decode()

    @classmethod
    def screenshot_file_to_base64(cls, file_full_path):
        """转为base64 编码数据

        @filename 完整文件路径
        """
        raw_data = ""
        try:
            with open(file_full_path, "rb") as f:
                raw_data = f.read()
        except IOError as err:
            print(err)
        return base64.b64encode(raw_data).decode()

    def _get_screenshot_path(self, filename):

        directory = self.screenshot_root_directory or self.SCREENSHOTS_DIR
        filename = filename.replace('/', os.sep)
        path = os.path.join(directory, filename)
        return path

    def _create_directory(self, path):

        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
