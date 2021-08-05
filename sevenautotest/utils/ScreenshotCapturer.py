# -*- coding:utf-8 -*-

import io
import os
import base64
import pyautogui
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
    def pyautogui_screenshot(cls, file_full_path):

        img = pyautogui.screenshot()
        try:
            img.save(file_full_path, "png")
        except ValueError:
            return False
        except IOError:
            return False
        finally:
            del img
        return True

    def _pil_screenshot(self, file_full_path):

        img = pyautogui.screenshot()
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

        if self.driver:
            return self.driver.get_screenshot_as_base64()
        img = pyautogui.screenshot()
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
