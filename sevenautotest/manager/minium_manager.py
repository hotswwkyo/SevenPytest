# -*- coding:utf-8 -*-
import os
import time
import datetime

from sevenautotest import settings
from sevenautotest.utils.ScreenshotCapturer import ScreenshotCapturer


class AbstractMiniumManager(object):

    DEVICE_INFO = {}
    CONFIG = None

    def __init__(self):

        self.mini = None
        self.native = None
        self.log_message_list = []

    def init_minium(self):

        raise NotImplementedError

    def set_config(self):

        raise NotImplementedError

    def release_minium(self):

        raise NotImplementedError

    @property
    def page(self):

        raise NotImplementedError

    def screenshot(self, name=None):

        raise NotImplementedError

    def set_minium(self):

        raise NotImplementedError

    def set_native(self):

        raise NotImplementedError


try:
    import minium
    from minium.framework import miniconfig

    class MiniumManager(AbstractMiniumManager):

        DEVICE_INFO = {}
        CONFIG = None

        def __init__(self):

            self.mini = None
            self.native = None
            self.log_message_list = []

        def init_minium(self):

            self.set_config()
            if not self.testconfig.report_usage:
                minium.wechatdriver.minium_log.existFlag = 1
            self.set_minium()
            self.set_native()

        def set_config(self):

            cls = self.__class__
            if cls.CONFIG is None:
                if settings.MINI_CONFIG_JSON_FILE and os.path.exists(settings.MINI_CONFIG_JSON_FILE):
                    cls.CONFIG = miniconfig.MiniConfig.from_file(settings.MINI_CONFIG_JSON_FILE)
                else:
                    print("default configure file did not exist! use default config")
                    cls.CONFIG = miniconfig.MiniConfig(settings.MINI_CONFIG)
            self.testconfig = miniconfig.MiniConfig(cls.CONFIG)

        def release_minium(self):

            if not self.testconfig.close_ide and self.mini:
                self.mini.shutdown()
            if self.testconfig.platform != 'ide' and not self.testconfig.close_ide:
                self.native.stop_wechat() if self.native else print("Native module has not start, there is no need to stop WeChat")
            if self.native:
                self.native.release()
            self.mini = None
            self.native = None

        @property
        def page(self):

            return self.mini.app.get_current_page()

        def screenshot(self, name=None):

            filename = "%s.%0d.jpg" % (
                datetime.datetime.now().strftime("%H%M%S"),
                int(time.time() * 1000) % 1000,
            )
            if name and isinstance(name, str):
                filename = '{}_{}'.format(name, filename)
            filepath = os.path.join(settings.SCREENSHOTS_DIR, filename)
            self.native.screen_shot(filepath)
            time.sleep(1)
            # minium 版本还不支持开发者工具模拟器截图，则调用屏幕截图
            if not os.path.exists(filepath):
                ScreenshotCapturer.pyautogui_screenshot(filepath)
            return filepath

        def set_minium(self):

            if self.mini is None:
                self.mini = minium.Minium(project_path=self.testconfig.project_path, test_port=self.testconfig.test_port, dev_tool_path=self.testconfig.dev_tool_path)
                if self.testconfig.enable_app_log:

                    def mini_log_added(message):
                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message["dt"] = dt
                        self.log_message_list.append(message)

                    self.mini.connection.register("App.logAdded", mini_log_added)
                    self.mini.app.enable_log()
            return self.mini

        def set_native(self):

            if self.native is None:
                self.native = minium.native.get_native_driver(self.testconfig.platform, self.testconfig.device_desire)
                if self.testconfig.platform != "ide" and not self.testconfig.close_ide:
                    self.set_minium()
                    self.native.start_wechat()
                    path = self.mini.enable_remote_debug(use_push=self.testconfig.use_push, connect_timeout=self.testconfig.remote_connect_timeout)
                    if not self.testconfig.use_push:
                        self.native.connect_weapp(path)
                        self.mini.connection.wait_for(method="App.initialized")

except ImportError as e:
    _import_error = e

    class MiniumManager(AbstractMiniumManager):
        def init_minium(self):
            raise _import_error

        def set_config(self):

            raise _import_error

        def release_minium(self):

            raise _import_error

        @property
        def page(self):

            raise _import_error

        def screenshot(self, name=None):

            raise _import_error

        def set_minium(self):

            raise _import_error

        def set_native(self):

            raise _import_error


WECHAT_MANAGER = MiniumManager()
