# SevenPytest
基于pytest实现测试用例收集方案、自定义参数化方案、页面元素定位数据存储方案、测试用例数据存储和维护方案，这样可直接进入到设计编写测试用例业务代码阶段，避免重复设计这些方案以及方案不统一导致维护复杂、困难的烦恼。实现了可设置用例执行顺序，且不会与pytest-depends插件的依赖排序冲突，这样配合pytest-depends就可以很好的实现测试用例间的依赖设置。修改定制并汉化了html测试报告，使报告显示我们关心的数据，并更加简洁、美观、易读。采用test object设计模式，以及引入链式编程，语义清晰。对selenium、appium、minium（微信小程序自动化测试库）以及WinAppDriver（微软官方提供的一款用于做Window桌面应用程序的界面（UI）自动化测试工具）做了封装集成，更好的支持桌面端web界面、移动端app界面、微信小程序界面以及Window桌面应用程序的界面（UI）的自动化测试。
>* 详解见：https://blog.csdn.net/hotswwkyo/article/details/103211805
## 一、页面封装
web页面和app页面封装应继承自根基础页面类BasePage。同时封装的页面类需要有两个内部类Elements（元素类）和Actions（动作类），分别用于封装页面的元素和页面动作。这两个内部类Elements（元素类）和Actions（动作类）应分别继承自类BasePage.Elements和BasePage.Actions。页面会自动实例化这两个类，分别赋给页面属性elements和actions。Elements（元素类）和Actions（动作类）这两个类实例都有一个page属性指向当前封装的页面，页面提供的元素查找方法与selenium和appium提供的方法相同。

* 页面元素类（Elements）需要继承自根页面元素类（BasePage.Elements），如果使用PageElementLocators装饰元素方法，则编写要求如下：
    >* 元素方法需要接收一个参数
    >* 使用PageElementLocators装饰器装饰元素方法，PageElementLocators 有两个参数file_name、file_dir_path。file_name元素定位器文件名，未指定则以页面类名作为文件名。file_dir_path元素定位器文件所在的目录路径，未指定则以settings.py配置文件的PAGE_ELEMENTS_LOCATORS_ROOT_DIR作为默认查找目录，装饰器会根据设置的目录去查找指定名称的元素定位器文件并根据元素方法名从文件中读取出方法对应的数据作为字典传递给被装饰元素方法。
    >* <em style="color:#3572A5;">PageElementLocators</em>参数file_name接收的元素定位器excel文件格中数据格式定义如下：
	>    1. 元素方法定位器区域的第一行，第一列是区域分隔符（使用 页面元素定位器 进行分隔），第二列是元素方法名称，第三列是元素名称
	>    2. 元素方法定位器区域的第二行是数据标题
	>    3. 元素方法定位器区域的第三行是数据<br>
	>    ![](https://github.com/hotswwkyo/SevenPytest/blob/master/img/page_element_locators.png)
* 页面动作类（Actions）需要继承自根页面元素类（BasePage.Actions）,当前动作方法不需要返回数据处理时，可以考虑返回动作实例本身（self），在编写用例业务的时候就可以使用链式编程<br>

* web页面封装示例：

```python
# -*- coding:utf-8 -*-
"""
登录页面示例
"""
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators


class LoginEmailPage(BasePage):
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def login_frame(self, locators):

            xpath = locators.get("login_frame")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def username(self, locators):
            """用户名输入框"""

            xpath = locators.get("用户名")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def password(self, locators):
            """密码输入框"""

            xpath = locators.get("密码")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def auto_login(self, locators):
            """下次自动登录复选框"""

            xpath = locators.get("下次自动登录")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def login(self, locators):
            """登录按钮"""

            xpath = locators.get("登录")
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def select_login_frame(self):
            """进入frame"""

            self.page.select_frame(self.page.elements.login_frame)
            return self

        def move_to_login_btn(self):

            self.page.action_chains.move_to_element(self.page.elements.login).perform()
            # self.page.action_chains.move_to_element_with_offset(self.page.elements.auto_login,0,0).perform()
            return self

        def username(self, name):
            """输入用户名"""

            self.page.elements.username.clear()
            self.page.elements.username.send_keys(name)
            return self

        def password(self, pwd):
            """输入密码"""

            self.page.elements.password.clear()
            self.page.elements.password.send_keys(pwd)
            return self

        def login(self):
            """点击登录按钮"""

            self.page.elements.login.click()
            return self

```
* app页面封装示例：
```python
# -*- coding:utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.android.nativekey import AndroidKey
from sevenautotest.utils import helper
from sevenautotest.utils import TestAssert as ta
from sevenautotest.basepage import BasePage
from sevenautotest.basepage import PageElementLocators as page_element_locators

__author__ = "si wen wei"


class SettlementFilmDetailPage(BasePage):
    """
    中影发行结算->影片信息页面
    """
    class Elements(BasePage.Elements):
        @property
        @page_element_locators()
        def film_info_view(self, locators):
            """影片信息区域
            """

            uia_string = locators.get("影片信息view")  # UiSelector().resourceId("filmInfo")
            return self.page.find_element_by_android_uiautomator(uia_string)

        @property
        @page_element_locators()
        def film_name_view(self, locators):
            """影片名称区域"""

            xpath = locators.get("影片名称view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def show_time_view(self, locators):
            """上映时间区域"""

            xpath = locators.get("上映时间view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            # return self.page.find_element_by_android_uiautomator(xpath, timeout=float(timeout))
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def settlement_box_office_view(self, locators):

            xpath = locators.get("结算票房view")
            timeout = locators.get("查找元素超时时间(秒)", "7")
            return self.page.find_element_by_xpath(xpath, timeout=float(timeout))

        @property
        @page_element_locators()
        def zhongying_pf_view(self, locators):
            """中影票房view"""

            xpath = locators.get("中影票房view")
            return self.page.find_element_by_android_uiautomator(xpath)

        @property
        @page_element_locators()
        def shouri_pf_view(self, locators):
            """首日票房view"""

            xpath = locators.get("首日票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def shouzhoumo__pf_view(self, locators):
            """首周末票房view"""

            xpath = locators.get("首周末票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def qian7tian_pf_view(self, locators):
            """前7天票房view"""

            xpath = locators.get("前7天票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def danrizuigao_pf_view(self, locators):
            """单日最高票房view"""

            xpath = locators.get("单日最高票房view")
            return self.page.find_element_by_xpath(xpath)

        @property
        @page_element_locators()
        def see_more_view(self, locators):
            """查看更多view"""

            xpath = locators.get("查看更多view")
            return self.page.find_element_by_xpath(xpath)

        @page_element_locators()
        def datetime_fx_view(self, locators, film_name):
            """发行有效日期view"""

            xpath = locators.get("发行有效日期view")
            xpath = xpath % film_name
            return self.page.find_element_by_xpath(xpath, parent=self.search_result_area)

        @page_element_locators()
        def film_type_fx_view(self, locators, film_name):
            """发行版本view"""

            xpath = locators.get("发行版本view")
            xpath = xpath % film_name
            return self.page.find_element_by_xpath(xpath, parent=self.search_result_area)

        @property
        @page_element_locators()
        def fx_detail_btn(self, locators):
            """进入发行信息详情页按钮"""

            xpath = locators.get("进入按钮")
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def swipe_to_select_year(self, year, direction="down", distance=70, limit_times=20, current_count=1):
            """选择年

            @param year 目标年份
            @param direction 首次滑动方向 down --- 向下   up --- 向上
            @param distance 每次滑动距离
            @param limit_times 递归次数
            @param current_count 当前递归计数
            """
            selector = self.page.elements.year_selector
            text_before_swipe = selector.get_attribute("text")

            if year == text_before_swipe:
                return self
            if current_count > limit_times:
                msg = "找不到: %s, 请检查" % year
                raise NoSuchElementException(msg)

            def _swipe_year_area(times=1):
                selector.click()
                view = self.sleep(2).page.elements.year_select_area
                x = view.location['x']
                y = view.location['y']
                height = view.size['height']
                width = view.size['width']
                start_x = x + width / 2
                start_y = y + height / 2
                end_x = start_x
                if direction.upper() == "down".upper():
                    end_y = start_y + distance
                else:
                    end_y = start_y - distance
                for n in range(times):
                    self.page.driver.swipe(start_x, start_y, end_x, end_y)
                self.click_confirm_btn()
                self.page.sleep(3)

            _swipe_year_area(1)
            text_after_swipe = selector.get_attribute("text")
            if year == text_after_swipe:
                return self
            if text_before_swipe == text_after_swipe:
                if direction.upper() == "down".upper():
                    direction = "up"
                else:
                    direction = "down"
            else:
                target_year = helper.cutout_prefix_digital(year)
                year_before_swipe = helper.cutout_prefix_digital(text_before_swipe)
                year_after_swipe = helper.cutout_prefix_digital(text_after_swipe)

                if target_year and year_before_swipe and year_after_swipe:
                    t = int(target_year)
                    a = int(year_after_swipe)
                    b = int(year_before_swipe)
                    if a > b:  # 当前方向滑动，数值变大
                        if t < a:  # 目标数值小于a数值，说明需要往数值小的方向滑动，改变方向
                            direction = "up" if direction.upper() == "down".upper() else "down"
                    else:
                        if t > a:
                            direction = "up" if direction.upper() == "down".upper() else "down"
                    _swipe_year_area(abs(t - a))
                    self.page.sleep(1)
            self.swipe_to_select_year(year, direction, distance, limit_times=limit_times, current_count=current_count + 1)
            return self

        def zhongying_pf_equals(self, box_office):
            """中影票房是否正确"""
            expected = box_office
            actual = self.page.elements.zhongying_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def shouri_pf_equals(self, box_office):
            """首日票房是否正确"""
            expected = box_office
            actual = self.page.elements.shouri_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def shouzhoumo_pf_equals(self, box_office):
            """首周末票房是否正确"""
            expected = box_office
            actual = self.page.elements.shouzhoumo__pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def qian7tian_pf_equals(self, box_office):
            """前7天票房是否正确"""
            expected = box_office
            actual = self.page.elements.qian7tian_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def danrizuigao_pf_equals(self, box_office):
            """单日最高票房是否正确"""
            expected = box_office
            actual = self.page.elements.danrizuigao_pf_view.get_attribute("text")
            ta.assert_equals(actual, expected)
            return self

        def input_film_name(self, film_name):
            """输入影片名称"""

            self.page.elements.film_name_inputbox.clear()
            self.page.elements.film_name_inputbox.send_keys(film_name)
            return self

        def click_confirm_btn(self):
            """点击确定按钮"""

            self.page.elements.confirm_btn.click()
            return self

        def click_cancel_btn(self):
            """点击取消按钮"""

            self.page.elements.cancel_btn.click()
            return self

        def click_search(self):
            self.page.press_keycode(AndroidKey.ENTER)  # SEARCH
            return self

        def click_film_item(self, film_name):
            """点击结算影片项"""
            self.page.elements.film_in_search_result_area(film_name).click()
            return self

```
## 二、微信小程序页面封装
微信小程序自动化测试需要下载并安装微信官方提供的自动化测试库minium，以及微信开发工具，同时还要获得小程序源码。安装官方指导文档配置完成后，就可以按照以下说明进行封装了。
微信小程序页面封装应继承自根基础页面类BaseMiniumPage。同样封装的页面类需要有两个内部类Elements（元素类）和Actions（动作类），分别用于封装页面的元素和页面动作。这两个内部类Elements（元素类）和Actions（动作类）应分别继承自类BaseMiniumPage.Elements和BaseMiniumPage.Actions。页面会自动实例化这两个类，分别赋给页面属性elements和actions。Elements（元素类）和Actions（动作类）这两个类实例都有一个page属性指向当前封装的页面，页面提供的两个与minium查找元素的同名方法：
>- <em style="color:#3572A5;">get_element(self, selector, inner_text=None, text_contains=None,value=None, max_timeout=20)</em>
>- <em style="color:#3572A5;">get_element(self, selector, inner_text=None, text_contains=None,value=None, max_timeout=20)</em>
* 微信小程序页面封装示例：
```python
# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class ADBasketPage(BaseMiniumPage):
    """ 广告篮页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def do_ad_btn(self):
            """去投放广告"""

            selector = '#cart'
            inner_text = '去投放广告'
            return self.page.get_element(selector).get_element('view').get_element('view').get_element('button', inner_text=inner_text)

        @property
        def tabbar(self):
            """首页下方tab工具栏"""

            selector = '.mp-tabbar'
            return self.page.get_element(selector)

        @property
        def home_tab(self):
            """首页 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "首页"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def ad_tab(self):
            """广告篮 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "广告篮"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def order_tab(self):
            """订单 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "订单"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def my_tab(self):
            """我的 标签"""

            selector = '.weui-tabbar__label'
            inner_text = "我的"
            return self.tabbar.get_element(selector, inner_text=inner_text)

        @property
        def _ad_cart(self):
            """广告购物车"""

            s = 'view>cart#cart'
            el_cart = self.page.get_element(s)
            el_cart.click()
            self.page.sleep(1)
            return el_cart

        def cinema_checkbox(self, cinema):
            """影院复选框

            Args:
                cinema: 影院
            """

            s1 = 'view.container.car>view.cinema-list>view.backgroud-float>view.flex-row>view.cinema-title'
            # 影院名
            s2 = 'text'
            # 复选框
            s8 = 'view>image.cart-icon'
            el_cts = self._ad_cart.get_elements(s1)
            el_cb = None
            for el_ct in el_cts:
                el_cinema = el_ct.get_element(s2)
                if el_cinema and el_cinema.inner_text == cinema:
                    el_cb = el_ct.get_element(s8)
                    if el_cb:
                        break
            return el_cb

        @property
        def all_schedules(self):
            """所有影院排期, 未调试，误用

            Args:
                cinema: 影院
            """

            s1 = 'view.container.car>view.cinema-list>view.backgroud-float'
            # 影院名
            s2 = 'view.flex-row>view.cinema-title>text.cinema-Name'
            # 放映日期
            s3 = 'view.cart--cinema-time'
            # 排期列表
            s4 = 'view.cart--cart-goods'
            # 影片名称
            s5 = 'view.cart-img>view.cart-message>view.name>text.filmName'
            # 放映时间
            s6 = 'view.cart-img>view.cart-message>view.common-flex>text.playTime'
            # 影厅
            s7 = 'view.cart-img>view.cart-message>view.common-flex>text.filmType'

            el_cinemaboxs = self._ad_cart.get_elements(s1)
            schedules = {}
            # {
            # 'el_cinema': {
            # 'el_showdate': [
            # (el_film, el_showtime, el_hall),...
            # ]
            # }
            # }
            for el_cinemabox in el_cinemaboxs:
                el_cinema = el_cinemabox.get_element(s2)
                if el_cinema:
                    cinema_schedules = {}  # 影院排期
                    el_cart_boxes = el_cinemabox.get_elements('view>view.cart--cart-box')
                    for el_cart_box in el_cart_boxes:
                        el_showdate = el_cinemabox.get_element(s3)
                        if not el_showdate:
                            continue
                        el_cart_goods = el_cart_box.get_element(s4)
                        one_day_schedules = []
                        for el_cart_good in el_cart_goods:
                            el_film = el_cart_good.get_element(s5)
                            el_showtime = el_cart_good.get_element(s6)
                            el_hall = el_cart_good.get_element(s7)
                            if el_film and el_showtime and el_hall:
                                one_day_schedules.append((el_film, el_showtime, el_hall))
                        cinema_schedules[el_showdate] = one_day_schedules
                    schedules[el_cinema] = cinema_schedules
            return schedules

        def schedule_checkbox(self, cinema, film, hall, showdate, showtime):
            """排期复选框

            Args:
                film: 影片
                cinema: 影院
                hall: 影厅
                showdate: 放映日期
                showtime: 放映时间
            """

            s1 = 'view.container.car>view.cinema-list>view.backgroud-float'
            # 影院名
            s2 = 'view.flex-row>view.cinema-title>text'
            # 放映日期
            s3 = 'view>view.cart--cart-box>view.cart--cinema-time'
            # 排期列表
            s4 = 'view>view.cart--cart-box>view.cart--cart-goods'
            # 影片名称
            s5 = 'view.cart-img>view.cart-message>view.name>text'
            # 放映时间
            s6 = 'view.cart-img>view.cart-message>view.common-flex>text'
            # 影厅
            s7 = 'view.cart-img>view.cart-message>view.common-flex>text'
            # 复选框
            s8 = 'view>image'
            el_cinemaboxs = self._ad_cart.get_elements(s1)
            el_cb = None
            for el_cinemabox in el_cinemaboxs:
                el_cinema = el_cinemabox.get_element(s2, inner_text=cinema)
                if el_cinema:
                    el_showdate = el_cinemabox.get_element(s3, inner_text=showdate)
                    if el_cinema and el_showdate:
                        el_goods = el_cinemabox.get_elements(s4)
                        for el_good in el_goods:

                            el_film = el_good.get_element(s5, inner_text=film)
                            el_showtime = el_good.get_element(s6, inner_text=showtime)
                            el_halls = el_good.get_elements(s7)
                            el_rhall = None
                            for el_hall in el_halls:
                                if el_hall.inner_text.strip().startswith(hall):
                                    el_rhall = el_hall
                                    break

                            if el_film and el_showtime and el_rhall:
                                el_cb = el_good.get_element(s8)
                                if el_cb:
                                    break
                if el_cb:
                    break
            return el_cb

        @property
        def select_all_btn(self):
            """全选按钮"""

            inner_text = '全选'
            s = 'view.container.car>view.cart-bottom>view.car-pay>view.cart-bottom-select>text'
            return self._ad_cart.get_element(s, inner_text=inner_text)

        @property
        def org_price(self):
            """原价结算金额"""

            inner_text = '原价结算'
            s1 = 'view.container.car>view.cart-bottom>view.car-pay>view.cart-bottom-pay>view.cart-btn'
            s2 = 'view'

            el_p_btn = None
            el_btns = self._ad_cart.get_elements(s1)
            for el_btn in el_btns:
                el_yj = el_btn.get_element(s2, inner_text=inner_text)
                if el_yj:
                    el_views = el_btn.get_elements(s2)
                    el_p_btn = el_views[0]
            return el_p_btn

        @property
        def org_price_btn(self):
            """原价结算按钮"""

            inner_text = '原价结算'
            s = 'view.container.car>view.cart-bottom>view.car-pay>view.cart-bottom-pay>view.cart-btn>view'
            return self._ad_cart.get_element(s, inner_text=inner_text)

        @property
        def pt_price(self):
            """拼团结算金额"""

            inner_text = '拼团结算'
            s1 = 'view.container.car>view.cart-bottom>view.car-pay>view.cart-bottom-pay>view.cart-btn'
            s2 = 'view'

            el_p_btn = None
            el_btns = self._ad_cart.get_elements(s1)
            for el_btn in el_btns:
                el_yj = el_btn.get_element(s2, inner_text=inner_text)
                if el_yj:
                    el_views = el_btn.get_elements(s2)
                    el_p_btn = el_views[0]
            return el_p_btn

        @property
        def pt_price_btn(self):
            """拼团结算按钮"""

            inner_text = '拼团结算'
            s = 'view.container.car>view.cart-bottom>view.car-pay>view.cart-bottom-pay>view.cart-btn>view'
            return self._ad_cart.get_element(s, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def click_do_ad_btn(self):
            """点击去投放广告按钮"""

            self.page.elements.do_ad_btn.click()
            return self

        def click_tabbar(self):
            """点击下方标签工具栏"""

            self.page.elements.tabbar.click()
            return self

        def click_home_tab(self):
            """点击下方首页标签"""

            self.page.elements.home_tab.click()
            return self

        def click_ad_tab(self):
            """点击下方广告篮标签"""

            self.page.elements.ad_tab.click()
            return self

        def click_order_tab(self):
            """点击下方订单标签"""

            self.page.elements.order_tab.click()
            return self

        def click_my_tab(self):
            """点击下方我的标签"""

            self.page.elements.my_tab.click()
            return self

        def click_cinema_checkbox(self, cinema):
            """点击 影院复选框"""

            self.page.elements.cinema_checkbox(cinema).click()
            return self

        def click_schedule_checkbox(self, cinema, film, hall, showdate, showtime):
            """点击 排期复选框"""

            self.page.elements.schedule_checkbox(cinema, film, hall, showdate, showtime).click()
            return self

        def select_all(self):
            """点击全选按钮"""

            self.page.elements.select_all_btn.click()
            return self

        def org_price_equals(self, price, prefix='￥'):
            """检查原价结算金额是否正确"""

            ptext = self.page.elements.org_price.inner_text
            a_price = ptext.strip().lstrip(prefix)
            if a_price != price:
                self.page.fail('原价结算金额实际({})显示与预期({})不等'.format(a_price, price))
            return self

        def click_org_price(self):
            """点击原价结算按钮"""

            self.page.elements.org_price_btn.click()
            return self

        def pt_price_equals(self, price, prefix='￥'):
            """检查拼团结算金额是否正确"""

            ptext = self.page.elements.pt_price.inner_text
            a_price = ptext.strip().lstrip(prefix)
            if a_price != price:
                self.page.fail('拼团结算金额实际({})显示与预期({})不等'.format(a_price, price))
            return self

        def click_pt_price(self):
            """点击拼团结算按钮"""

            self.page.elements.pt_price_btn.click()
            return self

```
## 三、接口封装

* 示例：

```python
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
from sevenautotest.utils.DataProvider import DataProvider as data_provider

__version__ = "1.0"
__author__ = "si wen wei"


class NeteaseCloudMusicApi(object):
    """网易云音乐接口封装"""
    def __init__(self, url):
        self.url = url

    @data_provider()
    def song_detail(self, apidata, song_id):
        """歌曲信息"""

        api_path = apidata.get("接口路径")
        payload = {"id": song_id, "ids": "[{}]".format(song_id)}
        res = requests.get(url=urljoin(self.url, api_path), params=payload)
        return res

    @data_provider()
    def singer_album(self, apidata, singer_id, offset=0, total=True, limit=5):
        """歌手专辑"""

        api_path = apidata.get("接口路径")
        full_path = urljoin(self.url, api_path)
        payload = {"id": singer_id, "offset": offset, "total": total, "limit": limit}
        res = requests.get(url=urljoin(full_path, singer_id), params=payload)
        return res

```

## 四、测试用例数据
测试用例数据存放excel文件中，文件名需以测试类名作为名称，统一放在主目录下的testdata目录下。数据在文件中以用例数据块的方式存储，数据块定义如下：
>* 所有行中的第一列是标记列，第一行第一列是数据块开始标记
>* 第一行: 用例名称信息(标记列的下一列是用例方法名称列，之后是用例名称列)
>* 第二行: 用例数据标题
>* 第三行 开始 每一行都是一组完整的测试数据直至遇见空行或者下一个数据块

>![](https://github.com/hotswwkyo/SevenPytest/blob/master/img/testcase_data_excel_file.png)

## 五、用例编写
测试用例业务代码需要放在包sevenautotest下的子包testcases下，编写规则如下：
* 测试用例类需要继承测试基类（BaseTestCase）
* 测试方法需要使用标记pytest.mark.testcase进行标记，才会被当作测试用例进行收集，使用位置参数设置用例名，关键字参数说明如下：
    >* enable - 控制是否执行该用例，布尔值，如果没有该关键字参数则默认为True
    >* priority - 设置用例执行优先级，控制用例的执行顺序，整型数值，如果没有该参数则不会调整该用例的执行顺序
    >* author - 自动化用例代码编写人
    >* editor - 自动化用例代码修改人
* 测试方法需要接收一个参数，参数化时框架会自动从测试数据文件取出的该方法测试数据作为字典传给该测试方法

* web页面自动化测试用例示例：

```python
# -*- coding:utf-8 -*-
import pytest
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.samples.qqemail.LoginEmailPage import LoginEmailPage


class LoginEmailPageTest(BaseTestCase):
    """
    登录页面测试示例
    """
    def setup_class(self):

        pass

    def setup_method(self):

        pass

    @pytest.mark.testcase("成功登陆测试", priority=1, enable=True, author="siwenwei", editor="")
    def test_successfully_login(self, testdata):

        name = testdata.get("用户名")
        pwd = testdata.get("密码")
        url = testdata.get("登录页面URL")

        page = LoginEmailPage()
        page.chrome().maximize_window().open_url(url).actions.select_login_frame().sleep(1).username(name).password(pwd).sleep(2).move_to_login_btn().sleep(10).login().sleep(3)
        page.screenshot("successfully login.png")
        page.sleep(3)

    def teardown_method(self):

        pass

    def teardown_class(self):

        self.DRIVER_MANAGER.close_all_drivers()
```

* app自动测试用例示例
```python
# -*- coding:utf-8 -*-
import pytest
from sevenautotest import settings
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.fxjs.LoginPage import LoginPage
from sevenautotest.testobjects.pages.apppages.fxjs.HomePage import HomePage
from sevenautotest.testobjects.pages.apppages.fxjs.SettlementMainPage import SettlementMainPage


class LoginPageTest(BaseTestCase):
    """中影发行结算登录页面测试"""
    def setup_class(self):
        self.desired_caps = settings.APP_DESIRED_CAPS
        self.server_url = settings.APPIUM_SERVER
        # adb shell am start -W -n com.zgdygf.zygfpfapp/io.dcloud.PandoraEntry

    def setup_method(self):

        pass

    @pytest.mark.testcase("成功登录发行结算app测试", priority=1, enable=True, author="siwenwei", editor="")
    def test_successfully_login(self, testdata):

        name = testdata.get("用户名")
        pwd = testdata.get("密码")

        page = LoginPage()
        page.open_app(self.server_url, desired_capabilities=self.desired_caps, implicit_wait_timeout=10)
        page.actions.click_continue_btn().sleep(2).click_confirm_btn().sleep(2).username(name).password(pwd).login().sleep(2).reminder().sleep(21)
        # HomePage().elements.settlement_tab
        HomePage().actions.sleep(2).click_settlement_tab()
        sp = SettlementMainPage()
        sp.actions.sleep(7).swipe_to_select_year("2019年").sleep(7).input_film_name("单行道").click_search().sleep(3)
        page.hide_keyboard()
        sp.actions.click_film_item("单行道")

    def teardown_method(self):

        pass

    def teardown_class(self):

        self.DRIVER_MANAGER.close_all_drivers()
```

* 接口自动化测试用例示例：

```python
# -*- coding:utf-8 -*-
import json
import pytest
from sevenautotest import settings
from sevenautotest.utils import TestAssert
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.apis.NeteaseCloudMusicApi import NeteaseCloudMusicApi


class NeteaseCloudMusicApiTest(BaseTestCase):
    """
    网易云音乐接口测试示例
    """
    def setup_class(self):

        self.api = NeteaseCloudMusicApi(settings.API_INFO[1][0])

    def setup_method(self):

        pass

    @pytest.mark.testcase("查询歌曲详情测试", priority=1, enable=True, author="siwenwei", editor="")
    def test_check_song_detail(self, testdata):

        song_id = testdata.get("歌曲id")
        e_name = testdata.get("预期歌曲名称")
        response = self.api.song_detail(song_id)
        res = json.loads(response.text)
        songs = res["songs"]
        song = songs[0]
        name = song["name"]
        if name != e_name:
            TestAssert.fail("%s != %s" % (name, e_name))

    @pytest.mark.testcase("查询歌手专辑测试", priority=2, enable=True, author="siwenwei", editor="")
    def test_get_singer_album(self, testdata):

        singer_id = testdata.get("歌手id")
        offset = testdata.get("offset")
        total = testdata.get("total")
        limit = testdata.get("limit")
        e_name = testdata.get("封面艺人名")
        response = self.api.singer_album(singer_id, offset=offset, total=total, limit=limit)
        res = json.loads(response.text)

        artist = res["artist"]
        name = artist["name"]
        if name != e_name:
            TestAssert.fail("%s != %s" % (name, e_name))

    def teardown_method(self):

        pass

    def teardown_class(self):

        pass
```
* 微信小程序自动化测试用例示例
```python
# -*- coding:utf-8 -*-
import pytest
from sevenautotest import settings
from sevenautotest.utils import helper
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.pages.apppages.yy.indexpage import IndexPage
from sevenautotest.testobjects.pages.apppages.yy.cinema_list_page import CinemaListPage
from sevenautotest.testobjects.pages.apppages.yy.my_adlist_page import MyAdListPage


class YuyanTest(BaseTestCase):
    """雨燕测试"""
    def setup_class(self):

        self.WECHAT_MANAGER.init_minium()

    def setup_method(self):
        pass

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>去上传广告片', priority=1, enable=True, author="siwenwei", editor="")
    def test_jump_page_of_click_upload_ad(self, testdata):

        fn_name = helper.get_caller_name()
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1).click_cinema_ad_btn()
        clpage = CinemaListPage()
        clpage.actions.sleep(1).screenshot('{}_影院列表_'.format(fn_name)).is_page_self(settings.URLS['影院列表']).upload_ad().sleep(2)
        p = MyAdListPage()
        p.actions.screenshot('{}_我的广告素材_'.format(fn_name)).is_page_self()

    @pytest.mark.testcase('广告投放界面->广告视频显示的正确性 - 影院列表>广告片显示>更换广告片', priority=2, enable=True, author="siwenwei", editor="")
    def test_change_ad_to_another_in_cinemalist(self, testdata):

        oad_name = testdata.get('广告名(原)')
        nad_name = testdata.get('广告名(新)')
        ipage = IndexPage(settings.URLS['首页'])
        ipage.actions.click_tabbar().sleep(1).click_home_tab().sleep(1).click_cinema_ad_btn()
        clpage = CinemaListPage()
        clpage.actions.sleep(1).is_page_self(settings.URLS['影院列表']).upload_ad().sleep(2)
        p = MyAdListPage()
        p.actions.is_page_self().click_ad_checkbox(oad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.change().sleep(1)
        p.actions.click_ad_checkbox(nad_name).sleep(1).to_launch().sleep(2)
        clpage.actions.find_ad_name(nad_name)

    def teardown_method(self):
        pass

    def teardown_class(self):

        self.WECHAT_MANAGER.release_minium()
```
## 六、执行测试
直接运行主目录下的TestRunner.py，也可以在命令行使用pytest命令执行
## 七、 测试报告
增加用例中文名称、测试数据、用例编写人等关键信息列，如图：
>![](https://github.com/hotswwkyo/SevenPytest/blob/master/img/html_report.png)
