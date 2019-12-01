# -*- coding:utf-8 -*-

"""

"""

import time
import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from uitest.browser import BrowserManager
from uitest.exceptions import NoOpenBrowser
from uitest.exceptions import WindowNotFound
from uitest.utils import helper
from uitest.utils import typetools
from uitest.utils.marker import AttributeMarker
from uitest.utils.marker import ConstAttributeMarker
from uitest.utils.AttributeManager import AttributeManager
from uitest.utils.ScreenshotCapturer import ScreenshotCapturer

__version__ = "1.0"
__author__ = "si wen wei"

class AbstractBasePage(AttributeManager):
    """
    
    """
    
    BROWSER_MANAGER     = AttributeMarker(BrowserManager(), True, "浏览器管理器")
    
    def __init__(self, browser=None, url=None, alias=None, timeout=0.0, *args, **kwargs):
        
        self._bm        = self.__class__.BROWSER_MANAGER
        
        if isinstance(browser, str):
            self.open_browser(browser, url, alias, *args, **kwargs)
        elif typetools.is_webdriver(browser):
            self._bm.register_browser(browser, alias)
        
        if isinstance(url, str) and self._bm.browser:
            self._bm.open_url(url)
            
        self.timeout    = timeout       
        
        self._build_elements()
        self._build_actions()
        self.init()
        
    def init(self):
        
        pass
    
    def _build_elements(self):
        
        self.elements   = self.__class__.Elements(self)
    
    def _build_actions(self):
        
        self.actions    = self.__class__.Actions(self)
    
    @property
    def browser(self):
    
        return self._bm.browser
    
    @property
    def browser_manager(self):
        
        return self._bm
        
    @property
    def browser_index(self):
        
        return self._bm.index
    
    def open_browser(self, browser_name, url=None, alias=None, *args, **kwargs):
        
        self._bm.open_browser(browser_name, url, alias, *args, **kwargs)
        return self
    
    def ie(self, url=None, alias=None, *args, **kwargs):
        
        return self.open_browser( BrowserManager.IE_NAME, url, alias, *args, **kwargs)
        
    def chrome(self, url=None, alias=None, *args, **kwargs):
        
        return self.open_browser( BrowserManager.CHROME_NAME, url, alias, *args, **kwargs)
        
    def firefox(self, url=None, alias=None, *args, **kwargs):
        
        return self.open_browser( BrowserManager.FIREFOX_NAME, url, alias, *args, **kwargs)

    def switch_browser(self, index_or_alias):
        
        self._bm.switch_browser(index_or_alias)
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
        @return         - WebElement - the element if it was found
        """
        
        if not (timeout and self._validate_timeout(timeout)):
            timeout = self.timeout
            
        if parent and self._is_webelement(parent):
            driver = parent.parent
        else:
            driver = self.browser
        message = "{} with locator '{}' not found".format(by, locator)
        try:
            element = WebDriverWait(driver, timeout).until(lambda x : x.find_element(by, locator))
        except TimeoutException as exc:
            message = message + "in {timeout}".format(timeout=timeout)
            screen = getattr(exc, 'screen', None)
            stacktrace = getattr(exc, 'stacktrace', None)
            raise TimeoutException(message, screen, stacktrace)
        except NoSuchWindowException as e:
            message = message + "," + e.msg
            screen = getattr(exc, 'screen', None)
            stacktrace = getattr(exc, 'stacktrace', None)
            raise NoSuchWindowException(message, screen, stacktrace)
        except Exception as e:
            print(message)
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
        message = "{} with locator '{}' not found.".format(by, locator)
        try:
            elements = WebDriverWait(driver, timeout).until(lambda x : x.find_elements(by, locator))
        except TimeoutException as t:
            message = message + "in {timeout}".format(timeout=timeout)
            screen = getattr(exc, 'screen', None)
            stacktrace = getattr(exc, 'stacktrace', None)
            raise TimeoutException(message, screen, stacktrace)
        except NoSuchWindowException as e:
            message = message + "," + e.message
            screen = getattr(exc, 'screen', None)
            stacktrace = getattr(exc, 'stacktrace', None)
            raise NoSuchWindowException(message, screen, stacktrace)
        except Exception as e:
            print(message)
            raise e
        else:
            return elements
            
    def sleep(self, milliseconds):
        """milliseconds the length of time to sleep in milliseconds"""
        seconds = milliseconds / 1000.000
        time.sleep(seconds)
        return self
        
    def wait_until_contains(self, text, timeout=None):
        """等待文本出现在当前页面"""
        
        locator = "//*contains(., %s)" % helper.escape_xpath_value(text)
        try:
            self.find_element_by_xpath(locator, timeout=timeout)
        except Exception:
            message = "Text '%s' did not appear in %s." % (text,timeout)
            raise TimeoutException(message)
        
    @staticmethod   
    def wait_until(condition, message="", timeout=None, poll_frequency=0.2, ignored_exceptions=None):
    
        exceptions = [NoSuchElementException]
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:
                exceptions.append(ignored_exceptions)
        _ignored_exceptions = tuple(exceptions)
        end_time            = time.time() + timeout
        not_found           = None
        while time.time() < end_time:       
            try:
                if condition():
                    return
            except _ignored_exceptions as err:
                not_found = str(err)
            else:
                not_found   = None
            time.sleep(poll_frequency)
        raise TimeoutException(not_found or message)
        
    def execute_script(sefl, script, *args):
        
        return self._bm.browser.execute_script(script, *args)
        
    def click_element_by_javascript(self, web_element):
        
        script = "arguments[0].click();"
        return self.execute_script(script, web_element)
        
    def scroll_to(self,xpos, ypos):
        """scroll to any position of an opened window of browser"""
        
        js_code = "window.scrollTo(%s, %s);" % (xpos, ypos)
        self.execute_script(js_code)
        
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
                page.screenshot("debug.png", r"E:\SevenPytest\screenshots")
        """
        return ScreenshotCapturer(self._bm.browser, screenshot_dir=screenshot_dir).screenshot(file_name)
        
    @property
    def title(self):
        
        self._bm.browser.title
        
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
        
        infos = {
            "handle": handle,
            "name": self.execute_script("return window.name;"),
            "title": self._bm.browser.title,
            "url": self._bm.browser.current_url
        }
        return infos
    
    def switch_window_by_title(self, title, matcher=None):
        """根据标题切换窗口
        
        @param matcher 匹配函数，接收两个参数，遍历传入每一个窗口的标题给第一个参数，要打开的窗口标题传给第二个参数，匹配返回True否则返回False
        """
        for map in self.window_infos_maps:          
            m_title     = map["title"]
            m_handle    = map["handle"]         
            if inspect.isfunction(matcher):
                if matcher(m_title, title):
                    self.switch_window(m_handle)
                    return
            else:
                if m_title == title:
                    self.switch_window(m_handle)
                    return
        message = "No window matching title(%s)" % title
        raise WindowNotFound(message)
        
    def switch_window_by_url(self, url, matcher=None):
        """根据url切换窗口
        
        @see select_window_by_url(self, url, matcher=None)
        """
        for map in self.window_infos_maps:          
            m_url       = map["url"]
            m_handle    = map["handle"]         
            if inspect.isfunction(matcher):
                if matcher(m_url, url):
                    self.switch_window(m_handle)
                    return
            else:
                if m_url == url:
                    self.switch_window(m_handle)
                    return
        message = "No window matching url(%s)" % url
        raise WindowNotFound(message)
    
    def close(self):
        """ Closes the current window.
        
        @see selenium.webdriver.remote.webdriver.close()
        """
        self._bm.browser.close()
        
    class Elements(object):
        
        def __init__(self, page):
            
            self.page = page
            
        def sleep(self, milliseconds):
            
            self.page.sleep(milliseconds)
            return self
        
    class Actions(object):
        
        def __init__(self, page):
            
            self.page = page
            
        def sleep(self, milliseconds):
            
            self.page.sleep(milliseconds)
            return self
 
if __name__ == "__main__":
    
    pass