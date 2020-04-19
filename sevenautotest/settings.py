# -*- coding: utf-8 -*-

"""
配置文件
"""

__version__ = "1.0"
__author__ = "si wen wei"

import os

# 手机app用户账号
APP_USER_ACCOUNT                        = "cs"

# 手机app用户密码
APP_USER_PASSWORD                       = "hy"

APPIUM_SERVER                           = "http://127.0.0.1:4723/wd/hub"

APP_DESIRED_CAPS                        = {'platformName': 'Android', # 平台名称
                                            'platformVersion': '10.0',  # 系统版本号
                                            'deviceName': 'P10 Plus',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                                            'appPackage': 'com.zgdygf.zygfpfapp',  # apk的包名
                                            'appActivity': 'io.dcloud.PandoraEntry',  # activity 名称
                                            #'automationName': "uiautomator2"
                                        }

#接口信息设置
API_INFO                                = [
                                            ("10.201.15.244",10021),
                                            ("http://music.163.com",)
                                        ]

#settings.py 所在目录路径
BASE_DIR                                = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR                             = os.path.dirname(BASE_DIR)

#浏览器驱动目录
DRIVERS_DIR                             = os.path.join(PROJECT_DIR, "drivers")

#谷歌浏览器驱动完整路径
CHROME_DRIVER_PATH                      = os.path.join(DRIVERS_DIR, "chrome", "chromedriver.exe")

#测试报告存放目录
REPORT_DIR                              = os.path.join(PROJECT_DIR, "report")

#测试用例数据目录
TEST_DATA_EXCEL_DIR                     = os.path.join(PROJECT_DIR, "testdata")

#测试用例代码目录
TESTCASES_DIR                           = os.path.join(BASE_DIR, "testcases")

#截图目录
SCREENSHOTS_DIR                         = os.path.join(PROJECT_DIR, "screenshots")

#封装的接口方法的基础数据根目录
API_DATA_ROOT_DIR                       = os.path.join(PROJECT_DIR, "apidata")

#页面元素定位器根目录
PAGE_ELEMENTS_LOCATORS_ROOT_DIR         = os.path.join(PROJECT_DIR, "locators")

#HTML测试报告文件名
HTML_REPORT_NAME                        = "autotest_report.html"

#HTML 测试报告完整路径
HTML_REPORT_FILE_PATH                   = os.path.join(REPORT_DIR, HTML_REPORT_NAME)

#python __init__.py file name
PY_INIT_FILE_NAME                       = "__init__.py"

#测试用例标记
TESTCASE_MARKER_NAME                    = "testcase"

#是否把报告添加到HTML报告上
ATTACH_SCREENSHOT_TO_HTML_REPORT        = True

#执行测试的pytest命令
PYTEST_COMMANDS                         = ["-s",'--html=%s' % HTML_REPORT_FILE_PATH, '--self-contained-html']