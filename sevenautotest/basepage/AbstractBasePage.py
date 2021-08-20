# -*- coding:utf-8 -*-
"""

"""

import time
import base64
import inspect
import subprocess
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from sevenautotest.manager import DriverManager
from sevenautotest.manager.app_helper import WinAppDriverHelper
from sevenautotest.exceptions import WindowNotFound
from sevenautotest.utils import helper
from sevenautotest.utils import typetools
from sevenautotest.utils.marker import AttributeMarker
from sevenautotest.utils.AttributeManager import AttributeManager
from sevenautotest.utils.ScreenshotCapturer import ScreenshotCapturer
from sevenautotest.utils.HtmlSelectElement import HtmlSelectElement

__version__ = "1.0"
__author__ = "si wen wei"


class AbstractBasePage(AttributeManager):
    """

    """
    KEYS = AttributeMarker(Keys, True, "键盘按键")
    DESKTOP_ALIAS = AttributeMarker("WindowDesktop", True, "创建的window桌面会话默认别名")
    DRIVER_MANAGER = AttributeMarker(DriverManager(), True, "Driver管理器")
    WIN_APP_DRIVER_HELPER = AttributeMarker(WinAppDriverHelper(), True, "启动和关闭WinAppDriver.exe助手")

    def __init__(self, browser=None, url=None, alias=None, timeout=0.0, *args, **kwargs):

        self._bm = self.__class__.DRIVER_MANAGER

        self._bm.script_timeout = kwargs.get("script_timeout", 5.0)
        self._bm.implicit_wait_timeout = kwargs.get("implicit_wait_timeout", 0.0)
        if isinstance(browser, str):
            self.open_browser(browser, url, alias, *args, **kwargs)
        elif typetools.is_webdriver(browser):
            self._bm.register_browser(browser, alias)

        if isinstance(url, str) and self._bm.browser:
            self._bm.open_url(url)

        self.timeout = timeout

        self._build_elements()
        self._build_actions()
        self.init()

    def init(self):

        pass

    def _build_elements(self):

        self.elements = self.__class__.Elements(self)

    def _build_actions(self):

        self.actions = self.__class__.Actions(self)

    @property
    def browser(self):

        return self._bm.browser

    @property
    def driver(self):

        return self._bm.driver

    @property
    def window_app(self):

        return self._bm.driver

    @property
    def action_chains(self):
        """动作链对象"""

        return ActionChains(self.driver)

    @property
    def driver_manager(self):

        return self._bm

    @property
    def index(self):

        return self._bm.index

    def startup_winappdriver(self, executable_path, output_stream=None, auto_close_output_stream=False):
        """启动WinAppDriver.exe"""

        self.WIN_APP_DRIVER_HELPER.startup_winappdriver(executable_path, output_stream, auto_close_output_stream)
        return self

    def shutdown_winappdriver(self):
        """关闭WinAppDriver.exe"""

        self.WIN_APP_DRIVER_HELPER.shutdown_winappdriver()
        return self

    def open_app(self, remote_url='http://127.0.0.1:4444/wd/hub', alias=None, desired_capabilities=None, implicit_wait_timeout=7.0, browser_profile=None, proxy=None, keep_alive=True, direct_connection=False):

        self._bm.open_app(command_executor=remote_url,
                          alias=alias,
                          desired_capabilities=desired_capabilities,
                          implicit_wait_timeout=implicit_wait_timeout,
                          browser_profile=browser_profile,
                          proxy=proxy,
                          keep_alive=keep_alive,
                          direct_connection=direct_connection)
        return self

    def open_window_app(self, remote_url="http://127.0.0.1:4723", desired_capabilities={}, alias=None, window_name=None, splash_delay=0, exact_match=True, desktop_alias=None):
        """ 创建 Windows 应用程序驱动程序会话

        Args:
            remote_url: WinAppDriver or Appium server url
            desired_capabilities:用于创建 Windows 应用程序驱动程序会话的功能
                app Application identifier or executable full path Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge

                appArguments Application launch arguments https://github.com/Microsoft/WinAppDriver

                appTopLevelWindow Existing application top level window to attach to 0xB822E2

                appWorkingDir 应用程序工作目录 (仅限经典应用程序) C:\\Temp

                platformName Target platform name Windows

                platformVersion Target platform version 1.0

            alias: 为创建的应用会话设置别名
            window_name: 要附加的窗口名称，通常在启动屏幕之后
            exact_match: 如果窗口名称不需要完全匹配，则设置为False
            desktop_alias: 为创建的桌面会话设置别名，将默认为“WindowDesktop”
        """

        if window_name:
            subprocess.Popen(desired_capabilities['app'])
            if splash_delay > 0:
                # print('Waiting %s seconds for splash screen' % splash_delay)
                self.sleep(splash_delay)
            self.switch_window_app_by_name(remote_url, alias=alias, window_name=window_name, exact_match=exact_match, desktop_alias=desktop_alias, **desired_capabilities)
        if "platformName" not in desired_capabilities:
            desired_capabilities["platformName"] = "Windows"
        if "forceMjsonwp" not in desired_capabilities:
            desired_capabilities["forceMjsonwp"] = True

        self._open_window_desktop(remote_url, desktop_alias)
        self.open_app(remote_url=str(remote_url), alias=alias, desired_capabilities=desired_capabilities)
        return self

    def switch_window_app(self, index_or_alias):

        self.switch_driver(index_or_alias)
        return self

    def switch_window_app_by_window_element(self, remote_url, window_element, alias=None, desktop_alias=None, **kwargs):

        desired_caps = kwargs
        window_name = window_element.get_attribute("Name")
        if not window_name:
            msg = 'Error connecting webdriver to window "' + window_name + '". \n'
        else:
            msg = 'Error connecting webdriver to window(which window element tag name is:{}). \n'.format(window_element.tag_name)
        window = hex(int(window_element.get_attribute("NativeWindowHandle")))
        if "app" in desired_caps:
            del desired_caps["app"]
        if "platformName" not in desired_caps:
            desired_caps["platformName"] = "Windows"
        if "forceMjsonwp" not in desired_caps:
            desired_caps["forceMjsonwp"] = True
        desired_caps["appTopLevelWindow"] = window
        try:
            self.open_app(remote_url=str(remote_url), alias=alias, desired_capabilities=desired_caps)
        except Exception as e:
            raise WindowNotFound(msg + str(e))

    def switch_window_app_by_name(self, remote_url, window_name, alias=None, timeout=5, exact_match=True, desktop_alias=None, **kwargs):

        desired_caps = kwargs
        self._open_window_desktop(remote_url, desktop_alias)
        window_xpath = '//Window[contains(@Name, "' + window_name + '")]'
        window_locator = window_name
        try:
            if exact_match:
                window = self.find_element_by_name(window_locator)
            else:
                window = self.find_element_by_xpath(window_xpath)
            # print('Window_name "%s" found.' % window_name)
            window = hex(int(window.get_attribute("NativeWindowHandle")))
        except Exception:
            try:
                if exact_match:
                    window = self.find_element_by_name(window_locator, timeout=timeout)
                else:
                    window = self.find_element_by_xpath(window_xpath, timeout=timeout)
                # print('Window_name "%s" found.' % window_name)
                window = hex(int(window.get_attribute("NativeWindowHandle")))
            except Exception as e:
                # print('Closing desktop session.')
                raise NoSuchWindowException('Error finding window "' + window_name + '" in the desktop session. ' 'Is it a top level window handle?' + '. \n' + str(e))
        if "app" in desired_caps:
            del desired_caps["app"]
        if "platformName" not in desired_caps:
            desired_caps["platformName"] = "Windows"
        if "forceMjsonwp" not in desired_caps:
            desired_caps["forceMjsonwp"] = True
        desired_caps["appTopLevelWindow"] = window
        # global application
        try:
            # print('Connecting to window_name "%s".' % window_name)
            self.open_app(remote_url=str(remote_url), alias=alias, desired_capabilities=desired_caps)
        except Exception as e:
            raise WindowNotFound('Error connecting webdriver to window "' + window_name + '". \n' + str(e))
        return self

    def get_sub_windows_of_desktop(self, remote_url, desktop_alias_or_index=None):

        self._open_window_desktop(remote_url, desktop_alias_or_index)
        el_wins = self.find_elements_by_xpath("//Window[@Name]", timeout=5)
        return el_wins

    def _open_window_desktop(self, remote_url, alias=None):
        """打开window桌面会话"""

        if not alias:
            alias = self.DESKTOP_ALIAS
        try:
            self.switch_driver(alias)
        except RuntimeError:
            desktop_capabilities = dict({"app": "Root", "platformName": "Windows", "deviceName": "Windows", "alias": alias, "newCommandTimeout": 3600, "forceMjsonwp": True})
            self.open_app(remote_url=str(remote_url), alias=alias, desired_capabilities=desktop_capabilities)
        return self.index

    def close_driver(self):
        self._bm.close_driver()
        return self

    def close_all_drivers(self):
        self._bm.close_all_drivers()
        return self

    def open_browser(self, browser_name, url=None, alias=None, *args, **kwargs):

        self._bm.open_browser(browser_name, url, alias, *args, **kwargs)
        return self

    def ie(self, url=None, alias=None, *args, **kwargs):

        return self.open_browser(DriverManager.IE_NAME, url, alias, *args, **kwargs)

    def chrome(self, url=None, alias=None, *args, **kwargs):

        return self.open_browser(DriverManager.CHROME_NAME, url, alias, *args, **kwargs)

    def firefox(self, url=None, alias=None, *args, **kwargs):

        return self.open_browser(DriverManager.FIREFOX_NAME, url, alias, *args, **kwargs)

    def switch_browser(self, index_or_alias):

        self._bm.switch_browser(index_or_alias)
        return self

    def switch_driver(self, index_or_alias):
        self._bm.switch_driver(index_or_alias)
        return self

    def close_browser(self):

        self._bm.close_browser()
        return self

    def close_all_browsers(self):

        self._bm.close_browser()
        return self

    def open_url(self, url):

        self._bm.open_url(url)
        return self

    def _is_webelement(self, element):

        return typetools.is_webelement(element)

    def _validate_timeout(self, timeout):

        return isinstance(timeout, (int, float))

    def maximize_window(self):

        self.browser.maximize_window()
        return self

    def minimize_window(self):

        self.browser.minimize_window()
        return self

    def find_element_by_id(self, element_id, timeout=None, parent=None):
        """Finds an element by id.

        @param element_id - The id of the element to be found.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage  element = driver.find_element_by_id('foo')
        """

        return self.find_element(by=By.ID, locator=element_id, timeout=timeout, parent=parent)

    def find_elements_by_id(self, element_id, timeout=None, parent=None):
        """
        Finds multiple elements by id.

        @param element_id - The id of the elements to be found.

        @return list of WebElement - a list with elements if any was found.  An empty list if not

        @usage  elements = driver.find_elements_by_id('foo')
        """

        return self.find_elements(by=By.ID, locator=element_id, timeout=timeout, parent=parent)

    def find_element_by_xpath(self, xpath, timeout=None, parent=None):
        """
        Finds an element by xpath.

        @param xpath - The xpath locator of the element to find.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage  element = driver.find_element_by_xpath('//div/td[1]')
        """

        return self.find_element(by=By.XPATH, locator=xpath, timeout=timeout, parent=parent)

    def find_elements_by_xpath(self, xpath, timeout=None, parent=None):
        """
        Finds multiple elements by xpath.

        @param xpath - The xpath locator of the elements to be found.

        @return list of WebElement - a list with elements if any was found.  An empty list if not

        @usage  elements = driver.find_elements_by_xpath("//div[contains(@class, 'foo')]")
        """

        return self.find_elements(by=By.XPATH, locator=xpath, timeout=timeout, parent=parent)

    def find_element_by_link_text(self, link_text, timeout=None, parent=None):
        """
        Finds an element by link text.

        @param link_text: The text of the element to be found.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage  element = driver.find_element_by_link_text('Sign In')
        """

        return self.find_element(by=By.LINK_TEXT, locator=link_text, timeout=timeout, parent=parent)

    def find_elements_by_link_text(self, link_text, timeout=None, parent=None):
        """
        Finds elements by link text.

        @param link_text: The text of the elements to be found.

        @return list of webelement - a list with elements if any was found.  an empty list if not

        @usage  elements = driver.find_elements_by_link_text('Sign In')
        """

        return self.find_elements(by=By.LINK_TEXT, locator=link_text, timeout=timeout, parent=parent)

    def find_element_by_partial_link_text(self, link_text, timeout=None, parent=None):
        """
        Finds an element by a partial match of its link text.

        @param link_text The text of the element to partially match on.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage element = driver.find_element_by_partial_link_text('Sign')
        """

        return self.find_element(by=By.PARTIAL_LINK_TEXT, locator=link_text, timeout=timeout, parent=parent)

    def find_elements_by_partial_link_text(self, link_text, timeout=None, parent=None):
        """
        Finds elements by a partial match of their link text.

        @param link_text: The text of the element to partial match on.

        @return list of webelement - a list with elements if any was found.  an empty list if not

        @usage:
            elements = driver.find_elements_by_partial_link_text('Sign')
        """

        return self.find_elements(by=By.PARTIAL_LINK_TEXT, locator=link_text, timeout=timeout, parent=parent)

    def find_element_by_name(self, name, timeout=None, parent=None):
        """
        Finds an element by name.

        @param name: The name of the element to find.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage
            element = driver.find_element_by_name('foo')
        """

        return self.find_element(by=By.NAME, locator=name, timeout=timeout, parent=parent)

    def find_elements_by_name(self, name, timeout=None, parent=None):
        """
        Finds elements by name.

        @param name: The name of the elements to find.

        @return list of webelement - a list with elements if any was found.  an empty list if not

        @usage:
            elements = driver.find_elements_by_name('foo')
        """

        return self.find_elements(by=By.NAME, locator=name, timeout=timeout, parent=parent)

    def find_element_by_tag_name(self, name, timeout=None, parent=None):
        """
        Finds an element by tag name.

        @param name - name of html tag (eg: h1, a, span)

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage
            element = driver.find_element_by_tag_name('h1')
        """

        return self.find_element(by=By.TAG_NAME, locator=name, timeout=timeout, parent=parent)

    def find_elements_by_tag_name(self, name, timeout=None, parent=None):
        """
        Finds elements by tag name.

        @param name - name of html tag (eg: h1, a, span)

        @return list of WebElement - a list with elements if any was found.  An empty list if not

        @usage
            elements = driver.find_elements_by_tag_name('h1')
        """

        return self.find_elements(by=By.TAG_NAME, locator=name, timeout=timeout, parent=parent)

    def find_element_by_class_name(self, name, timeout=None, parent=None):
        """
        Finds an element by class name.

        @param name The class name of the element to find.

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage:
            element = driver.find_element_by_class_name('foo')
        """

        return self.find_element(by=By.CLASS_NAME, locator=name, timeout=timeout, parent=parent)

    def find_elements_by_class_name(self, name, timeout=None, parent=None):
        """
        Finds elements by class name.

        @param name The class name of the elements to find.

        @return list of WebElement - a list with elements if any was found.  An empty list if not

        @usage
            elements = driver.find_elements_by_class_name('foo')
        """

        return self.find_elements(by=By.CLASS_NAME, locator=name, timeout=timeout, parent=parent)

    def find_element_by_css_selector(self, css_selector, timeout=None, parent=None):
        """
        Finds an element by css selector.

        @param css_selector - CSS selector string, ex: 'a.nav#home'

        @return WebElement - the element if it was found

        @raise NoSuchElementException - if the element wasn't found

        @usage
            element = driver.find_element_by_css_selector('#foo')
        """

        return self.find_element(by=By.CSS_SELECTOR, locator=css_selector, timeout=timeout, parent=parent)

    def find_elements_by_css_selector(self, css_selector, timeout=None, parent=None):
        """
        Finds elements by css selector.

        @param css_selector - CSS selector string, ex: 'a.nav#home'

        @return list of WebElement - a list with elements if any was found.  An empty list if not

        @usage
            elements = driver.find_elements_by_css_selector('.foo')
        """

        return self.find_elements(by=By.CSS_SELECTOR, locator=css_selector, timeout=timeout, parent=parent)

    def find_element(self, by=By.ID, locator=None, timeout=None, parent=None):
        """
        查找匹配的元素

        @param by       - 查找方式
        @param locator  - 元素定位器
        @param timeout  - 查找元素超时时间
        @param parent   - 父元素,提供则从父元素下查找
        @raise NoSuchElementException - if the element wasn't found
        @raise TimeoutException - if the element wasn't found when time out
        @return         - WebElement - the element if it was found
        """

        if not (timeout and self._validate_timeout(timeout)):
            timeout = self.timeout

        if parent and self._is_webelement(parent):
            driver = parent.parent
        else:
            driver = self.browser

        # 如果设置的超时时间无效或者超时时间小于0，则不会执行超时
        if not (self._validate_timeout(timeout) and timeout > 0):
            return driver.find_element(by, locator)
        message = "{} with locator '{}' not found".format(by, locator)
        try:
            element = WebDriverWait(driver, timeout).until(lambda x: x.find_element(by, locator))
        except TimeoutException as exc:
            message = message + "in {timeout}".format(timeout=timeout)
            screen = getattr(exc, 'screen', None)
            stacktrace = getattr(exc, 'stacktrace', None)
            raise TimeoutException(message, screen, stacktrace)
        except NoSuchWindowException as e:
            message = message + "," + e.msg
            screen = getattr(e, 'screen', None)
            stacktrace = getattr(e, 'stacktrace', None)
            raise NoSuchWindowException(message, screen, stacktrace)
        except Exception as e:
            raise e
        else:
            return element

    def find_elements(self, by=By.ID, locator=None, timeout=None, parent=None):
        """
        查找所有匹配的元素

        @param by - 查找方式
        @param locator - 元素定位器
        @param timeout - 查找元素超时时间
        @param parent - 父元素,提供则从父元素下查找
        @return  list of WebElement - a list with elements if any was found. An empty list if not
        """

        if not (timeout and self._validate_timeout(timeout)):
            timeout = self.timeout

        if parent and self._is_webelement(parent):
            driver = parent.parent
        else:
            driver = self.browser
        # 如果设置的超时时间无效或者超时时间小于0，则不会执行超时
        if not (self._validate_timeout(timeout) and timeout > 0):
            return driver.find_elements(by, locator)
        message = "{} with locator '{}' not found.".format(by, locator)
        try:
            elements = WebDriverWait(driver, timeout).until(lambda x: x.find_elements(by, locator))
        except TimeoutException as t:
            message = message + "in {timeout}".format(timeout=timeout)
            screen = getattr(t, 'screen', None)
            stacktrace = getattr(t, 'stacktrace', None)
            # raise TimeoutException(message, screen, stacktrace)
            # print(message)
            return []
        except NoSuchWindowException as e:
            message = message + "," + e.message
            screen = getattr(e, 'screen', None)
            stacktrace = getattr(e, 'stacktrace', None)
            raise NoSuchWindowException(message, screen, stacktrace)
        except Exception as e:
            raise e
        else:
            return elements

    def find_element_by_ios_uiautomation(self, uia_string, timeout=None):
        """Finds an element by uiautomation in iOS.

        Args:
            uia_string (str): The element name in the iOS UIAutomation library

        Usage:
            driver.find_element_by_ios_uiautomation('.elements()[1].cells()[2]')

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.IOS_UIAUTOMATION, locator=uia_string, timeout=timeout, parent=None)

    def find_elements_by_ios_uiautomation(self, uia_string, timeout=None):
        """Finds elements by uiautomation in iOS.

        Args:
            uia_string: The element name in the iOS UIAutomation library

        Usage:
            driver.find_elements_by_ios_uiautomation('.elements()[1].cells()[2]')

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.IOS_UIAUTOMATION, locator=uia_string, timeout=timeout, parent=None)

    def find_element_by_ios_predicate(self, predicate_string, timeout=None):
        """Find an element by ios predicate string.

        Args:
            predicate_string (str): The predicate string

        Usage:
            driver.find_element_by_ios_predicate('label == "myLabel"')

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.IOS_PREDICATE, locator=predicate_string, timeout=timeout, parent=None)

    def find_elements_by_ios_predicate(self, predicate_string, timeout=None):
        """Finds elements by ios predicate string.

        Args:
            predicate_string (str): The predicate string

        Usage:
            driver.find_elements_by_ios_predicate('label == "myLabel"')

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.IOS_PREDICATE, locator=predicate_string, timeout=timeout, parent=None)

    def find_element_by_ios_class_chain(self, class_chain_string, timeout=None):
        """Find an element by ios class chain string.

        Args:
            class_chain_string (str): The class chain string

        Usage:
            driver.find_element_by_ios_class_chain('XCUIElementTypeWindow/XCUIElementTypeButton[3]')

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.IOS_CLASS_CHAIN, locator=class_chain_string, timeout=timeout, parent=None)

    def find_elements_by_ios_class_chain(self, class_chain_string, timeout=None):
        """Finds elements by ios class chain string.

        Args:
            class_chain_string (str): The class chain string

        Usage:
            driver.find_elements_by_ios_class_chain('XCUIElementTypeWindow[2]/XCUIElementTypeAny[-2]')

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.IOS_CLASS_CHAIN, locator=class_chain_string, timeout=timeout, parent=None)

    def find_element_by_android_uiautomator(self, uia_string, timeout=None):

        return self.find_element(by=MobileBy.ANDROID_UIAUTOMATOR, locator=uia_string, timeout=timeout, parent=None)

    def find_elements_by_android_uiautomator(self, uia_string, timeout=None):

        return self.find_elements(by=MobileBy.ANDROID_UIAUTOMATOR, locator=uia_string, timeout=timeout, parent=None)

    def find_element_by_android_viewtag(self, tag, timeout=None):
        """Finds element by [View#tags](https://developer.android.com/reference/android/view/View#tags) in Android.

        It works with [Espresso Driver](https://github.com/appium/appium-espresso-driver).

        Args:
            tag (str): The tag name of the view to look for

        Usage:
            driver.find_element_by_android_viewtag('a tag name')

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.ANDROID_VIEWTAG, locator=tag, timeout=timeout, parent=None)

    def find_elements_by_android_viewtag(self, tag, timeout=None):
        """Finds element by [View#tags](https://developer.android.com/reference/android/view/View#tags) in Android.

        It works with [Espresso Driver](https://github.com/appium/appium-espresso-driver).

        Args:
            tag (str): The tag name of the view to look for

        Usage:
            driver.find_elements_by_android_viewtag('a tag name')

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.ANDROID_VIEWTAG, locator=tag, timeout=timeout, parent=None)

    def find_element_by_image(self, img_path, timeout=None):
        """Finds a portion of a screenshot by an image.

        Uses driver.find_image_occurrence under the hood.

        Args:
            img_path (str): a string corresponding to the path of a image

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        with open(img_path, 'rb') as i_file:
            b64_data = base64.b64encode(i_file.read()).decode('UTF-8')

        return self.find_element(by=MobileBy.IMAGE, locator=b64_data, timeout=timeout, parent=None)

    def find_elements_by_image(self, img_path, timeout=None):
        """Finds a portion of a screenshot by an image.

        Uses driver.find_image_occurrence under the hood. Note that this will
        only ever return at most one element

        Args:
            img_path (str): a string corresponding to the path of a image

        Return:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        with open(img_path, 'rb') as i_file:
            b64_data = base64.b64encode(i_file.read()).decode('UTF-8')

        return self.find_elements(by=MobileBy.IMAGE, locator=b64_data, timeout=timeout, parent=None)

    def find_element_by_accessibility_id(self, accessibility_id, timeout=None):
        """Finds an element by accessibility id.

        Args:
            accessibility_id (str): A string corresponding to a recursive element search using the
                Id/Name that the native Accessibility options utilize

        Usage:
            driver.find_element_by_accessibility_id()

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.ACCESSIBILITY_ID, locator=accessibility_id, timeout=timeout, parent=None)

    def find_elements_by_accessibility_id(self, accessibility_id, timeout=None):
        """Finds elements by accessibility id.

        Args:
            accessibility_id (str): a string corresponding to a recursive element search using the
                Id/Name that the native Accessibility options utilize

        Usage:
            driver.find_elements_by_accessibility_id()

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.ACCESSIBILITY_ID, locator=accessibility_id, timeout=timeout, parent=None)

    def find_element_by_custom(self, selector, timeout=None):
        """Finds an element in conjunction with a custom element finding plugin

        Args:
            selector (str): a string of the form "module:selector", where "module" is
                the shortcut name given in the customFindModules capability, and
                "selector" is the string that will be passed to the custom element
                finding plugin itself

        Usage:
            driver.find_element_by_custom("foo:bar")

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        return self.find_element(by=MobileBy.CUSTOM, locator=selector, timeout=timeout, parent=None)

    def find_elements_by_custom(self, selector, timeout=None):
        """Finds elements in conjunction with a custom element finding plugin

        Args:
            selector: a string of the form "module:selector", where "module" is
                the shortcut name given in the customFindModules capability, and
                "selector" is the string that will be passed to the custom element
                finding plugin itself

        Usage:
            driver.find_elements_by_custom("foo:bar")

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        return self.find_elements(by=MobileBy.CUSTOM, locator=selector, timeout=timeout, parent=None)

    def sleep(self, seconds):
        """seconds the length of time to sleep in seconds"""
        time.sleep(seconds)
        return self

    def wait_until_contains(self, text, timeout=None):
        """等待文本出现在当前页面"""

        locator = "//*contains(., %s)" % helper.escape_xpath_value(text)
        try:
            self.find_element_by_xpath(locator, timeout=timeout)
        except Exception:
            message = "Text '%s' did not appear in %s." % (text, timeout)
            raise TimeoutException(message)

    @staticmethod
    def wait_until(callable_method, message="", timeout=None, poll_frequency=0.2, ignored_exceptions=None):

        if timeout is None:
            timeout = 0.0
        exceptions = [NoSuchElementException]
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:
                exceptions.append(ignored_exceptions)
        _ignored_exceptions = tuple(exceptions)
        end_time = time.time() + timeout
        not_found = None
        while True:
            try:
                if callable_method():
                    return
            except _ignored_exceptions as err:
                not_found = str(err)
            else:
                not_found = None
            if time.time() > end_time:
                break
            time.sleep(poll_frequency)
        raise TimeoutException(not_found or message)

    def execute_script(self, script, *args):

        return self._bm.browser.execute_script(script, *args)

    def click_element_by_javascript(self, web_element):

        script = "arguments[0].click();"
        return self.execute_script(script, web_element)

    def scroll_to(self, xpos, ypos):
        """scroll to any position of an opened window of browser"""

        js_code = "window.scrollTo(%s, %s);" % (xpos, ypos)
        self.execute_script(js_code)

    def scroll_into_view(self, web_element):

        js_code = 'arguments[0].scrollIntoView();'
        self.execute_script(js_code, web_element)

    def scroll_to_bottom(self):

        bottom = self.execute_script("return document.body.scrollHeight;")
        self.scroll_to(0, bottom)

    def scroll_to_top(self):

        self.scroll_to(0, 0)

    def drag_and_drop(self, source, target):

        ac = ActionChains(self._bm.browser)
        ac.drag_and_drop(source, target).perform()

    def screenshot(self, file_name, screenshot_dir=None):
        """截图并保存

        @param file_name 截图文件名
        @param screenshot_dir 截图存放目录，不设置则使用settings.SCREENSHOTS_DIR
        @usage
                page.screenshot("debug.png")
                page.screenshot("debug.png", "E:\\SevenPytest\\screenshots")
        """
        return ScreenshotCapturer(self._bm.browser, screenshot_dir=screenshot_dir).screenshot(file_name)

    @property
    def browser_session_id(self):
        """Returns the currently active browser session id"""

        return self._bm.browser.session_id

    @property
    def source(self):
        """Returns the entire HTML source of the current page or frame."""

        return self._bm.browser.page_source

    @property
    def title(self):
        """Returns the title of the current page."""

        return self._bm.browser.title

    @property
    def active_element(self):
        """Returns the element with focus, or BODY if nothing has focus.

        @see selenium.webdriver.remote.switch_to.SwitchTo.active_element
        @usage element = page.active_element
        """
        return self._bm.browser.switch_to.active_element

    @property
    def alert(self):
        """Switches focus to an alert on the page.

        @see selenium.webdriver.remote.switch_to.SwitchTo.alert
        @usage alert = page.alert
        """
        return self._bm.browser.switch_to.alert

    def select_frame(self, reference):
        """切换frame

        @param reference frame id name index 或 webelement 对象
        @see selenium.webdriver.remote.switch_to.SwitchTo.frame()
        @usage page.select_frame()
        """
        self._bm.browser.switch_to.frame(reference)

    def default_frame(self):
        """ Switch focus to the default frame.

        @see selenium.webdriver.remote.switch_to.SwitchTo.default_content()
        @usage page.default_frame()
        """
        self._bm.browser.switch_to.default_content()
        return self

    def parent_frame(self):
        """嵌套frame时，可以从子frame切回父frame

        @see selenium.webdriver.remote.switch_to.SwitchTo.parent_frame()
        @usage page.parent_frame()
        """

        self._bm.browser.switch_to.parent_frame()

    @property
    def current_window_handle(self):

        return self._bm.browser.current_window_handle

    @property
    def window_handles(self):

        return self._bm.browser.window_handles

    def switch_window(self, window_name_or_handle):
        """切换浏览器窗口

        @param window_name_or_handle 窗口句柄或窗口名
        """
        self._bm.browser.switch_to.window(window_name_or_handle)

    def switch_current_window(self):
        """切换到当前浏览器"""

        self.switch_window(self.current_window_handle)
        return self

    @property
    def window_infos_maps(self):
        """所有窗口信息

        @return 返回列表 [{"handle":window handle, "name": window name, "title": window title, "url": window url}, ...]
        """
        infos_maps = []
        try:
            source_handle = self.current_window_handle
        except NoSuchWindowException:
            source_handle = None
        try:
            for handle in self.window_handles:
                self._bm.browser.switch_to.window(handle)
                infos_maps.append(self._get_window_infos_map(handle))
        finally:
            if source_handle:
                self._bm.browser.switch_to.window(source_handle)
        return infos_maps

    def _get_window_infos_map(self, handle):

        title = self.driver.title
        try:
            name = self.execute_script("return window.name;")
        except Exception:
            name = title
        try:
            current_url = self._bm.browser.current_url
        except Exception:
            current_url = None

        infos = {"handle": handle, "name": name, "title": title, "url": current_url}
        return infos

    def switch_window_by_title(self, title, matcher=None, timeout=None):
        """根据标题切换窗口

        Args:
            title: 窗口标题
            matcher: 匹配函数，接收两个参数，遍历传入每一个窗口的标题给第一个参数，要打开的窗口标题传给第二个参数，匹配返回True否则返回False
            timeout: 超时时间
        """
        def _switch_window_by_title():
            be_found = False
            for win_handle in self.window_handles:
                self.switch_window(win_handle)
                info = self._get_window_infos_map(win_handle)
                if inspect.isfunction(matcher):
                    if matcher(info["title"], title):
                        be_found = True
                        break
                else:
                    if info["title"] == title:
                        be_found = True
                        break
            return be_found

        message = "No window matching title(%s)" % title
        self.wait_until(_switch_window_by_title, message=message, timeout=timeout)
        return self

    def switch_window_by_url(self, url, matcher=None, timeout=None):
        """根据url切换窗口

        @see select_window_by_url(self, url, matcher=None)
        """
        def _switch_window_by_url():
            be_found = False
            for win_handle in self.window_handles:
                self.switch_window(win_handle)
                info = self._get_window_infos_map(win_handle)
                if inspect.isfunction(matcher):
                    if matcher(info["url"], url):
                        be_found = True
                        break
                else:
                    if info["url"] == url:
                        be_found = True
                        break
            return be_found

        message = "No window matching url(%s)" % url
        self.wait_until(_switch_window_by_url, message=message, timeout=timeout)
        return self

    def set_window_size(self, width, height, window_handle='current'):
        """Sets current windows size to given ``width`` and ``height``

        @see WebDriver.set_window_size(self, width, height, windowHandle='current')
        """

        self._bm.browser.set_window_size(width, height, window_handle)
        return self

    def get_window_size(self, window_handle='current'):
        """Gets the width and height of the current window.

        @see WebDriver.get_window_size(self, windowHandle='current')
        """
        return self._bm.browser.get_window_size(window_handle)

    def set_window_position(self, x, y, window_handle='current'):

        self._bm.browser.set_window_position(self, x, y, window_handle)
        return self

    def get_window_position(self, window_handle='current'):

        return self._bm.browser.get_window_position(window_handle)

    def refresh(self):
        """刷新当前页面"""

        self.browser.refresh()
        return self

    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        self.driver.hide_keyboard(key_name=key_name, key=key, strategy=strategy)
        return self

    def keyevent(self, keycode, metastate=None):
        """Sends a keycode to the android device.

        @see appium.webdriver.exceptions.keyboard.Keyboard.keyevent
        """
        self.driver.keyevent(keycode, metastate=metastate)
        return self

    def press_keycode(self, keycode, metastate=None, flags=None):
        """Sends a keycode to the device.

        Android only. Possible keycodes can be found in http://developer.android.com/reference/android/view/KeyEvent.html
        @see appium.webdriver.exceptions.keyboard.Keyboard.press_keycode
        """
        self.driver.press_keycode(keycode, metastate=metastate, flags=flags)
        return self

    def create_select_element_wrapper(self, select_element):
        """创建操作html select 元素的包装器

        提供以下属性：
            options 返回select元素的所有选项
            all_selected_options 返回所有被选中的选项
            first_selected_option 第一个选中项

        提供以下方法：
            select_by_value(value) 通过选项中的value属性值选中选项
            select_by_index(index)
            select_by_visible_text(text) 通过选项中的文本选中选项 - <option>text</option>

            deselect_all()
            deselect_by_value(value)
            deselect_by_index(index)
            deselect_by_visible_text(text)

        @see selenium.webdriver.support.select.Select
        @see uitest.utils.HtmlSelectElement.HtmlSelectElement
        """

        return HtmlSelectElement(select_element)

    def close(self):
        """ Closes the current window.

        @see selenium.webdriver.remote.webdriver.close()
        """
        self._bm.browser.close()

    def is_element_enabled(self, element):
        """判断元素是否可用"""

        return (element.is_enabled() and element.get_attribute("readonly") is None)

    def get_value(self, element):

        return element.get_attribute("value")

    def raise_no_such_element_exc(self, message):

        raise NoSuchElementException(message)

    class Elements(object):
        def __init__(self, page):

            self.page = page

        def sleep(self, seconds):
            """延时"""

            self.page.sleep(seconds)
            return self

    class Actions(object):
        def __init__(self, page):

            self.page = page

        def sleep(self, seconds):
            """延时"""

            self.page.sleep(seconds)
            return self

        def turn_to_page(self, page_number):
            """翻页， 由具体页面实现"""

            raise NotImplementedError


if __name__ == "__main__":

    pass
