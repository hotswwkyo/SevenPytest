# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class HomePage(BasePage):
    """雨燕管理后台索引页面"""
    @classmethod
    def is_opened(cls, el_menu):
        """判断菜单是否处于展开状态"""

        if el_menu.tag_name.lower() != 'li'.lower():
            el_menu = el_menu.find_element_by_xpath('./ancestor::li')
        if el_menu.get_attribute('class').find('ant-menu-submenu-open') == -1:  # 菜单是收缩状态
            return False
        else:
            return True

    @classmethod
    def open_or_shrink(cls, el_menu, to_open=True):
        """展开或者收缩 菜单

        Args:
           el_menu: 菜单元素
           to_open: True - 展开  False - 收缩
        """

        if cls.is_opened(el_menu):
            if not to_open:
                el_menu.click()
        else:
            if to_open:
                el_menu.click()

    class Elements(BasePage.Elements):
        @property
        def home(self):
            """左侧菜单 首页"""

            menu = '首页'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/a/span[normalize-space()="{menu}"]'.format(menu=menu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order(self):
            """左侧菜单 订单"""

            menu = '订单'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]'.format(menu=menu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order_manager(self):
            """左侧子菜单 订单管理"""

            menu = '订单'
            submenu = '订单管理'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/div//span[normalize-space()="{submenu}"]'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order_list(self):
            """左侧二级子菜单 订单列表"""

            menu = '订单'
            submenu = '订单管理'
            level2 = '订单列表'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/div//span[normalize-space()="{submenu}"]/ancestor::li/ul/li/a/span[normalize-space()="{level2}"]/parent::*'.format(
                menu=menu, submenu=submenu, level2=level2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order_settings(self):
            """左侧二级子菜单 订单设置"""

            menu = '订单'
            submenu = '订单管理'
            level2 = '订单设置'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/div//span[normalize-space()="{submenu}"]/ancestor::li/ul/li/a/span[normalize-space()="{level2}"]/parent::*'.format(
                menu=menu, submenu=submenu, level2=level2)
            return self.page.find_element_by_xpath(xpath)

        @property
        def order_refund(self):
            """左侧子菜单 订单退款"""

            menu = '订单'
            submenu = '订单退款'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/div//span[normalize-space()="{submenu}"]'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def data(self):
            """左侧菜单 数据"""

            menu = '数据'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]'.format(menu=menu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def userlist(self):
            """左侧子菜单 用户列表"""

            menu = '数据'
            submenu = '用户列表'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def labelrule(self):
            """左侧子菜单 标签规则"""

            menu = '数据'
            submenu = '标签规则'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def adlist(self):
            """左侧子菜单 广告片列表"""

            menu = '数据'
            submenu = '广告片列表'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def cinema_manage(self):
            """左侧子菜单 影院管理"""

            menu = '数据'
            submenu = '影院管理'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def film_manage(self):
            """左侧子菜单 影片管理"""

            menu = '数据'
            submenu = '影片管理'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def ad_place_manage(self):
            """左侧子菜单 广告位管理"""

            menu = '数据'
            submenu = '广告位管理'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::div/parent::li/ul/li/a//span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def audit(self):
            """左侧菜单 审核"""

            menu = '审核'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::*'.format(
                menu=menu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def audit_tasklist(self):
            """左侧子菜单 审核任务列表"""

            menu = '审核'
            submenu = '审核任务列表'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/ancestor::li/ul/li/a/span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def cinema_audit_trail(self):
            """左侧子菜单 影院审核跟踪"""

            menu = '审核'
            submenu = '影院审核跟踪'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/ancestor::li/ul/li/a/span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def audit_settings(self):
            """左侧子菜单 审核设置"""

            menu = '审核'
            submenu = '审核设置'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/ancestor::li/ul/li/a/span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def spread(self):
            """左侧菜单 推广"""

            menu = '推广'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/parent::*'.format(
                menu=menu)
            return self.page.find_element_by_xpath(xpath)

        @property
        def haoyouzhuli(self):
            """左侧子菜单 好友助力"""

            menu = '推广'
            submenu = '好友助力'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-sider-children")]/div[contains(@class,"logo")]/parent::div/ul[@role="menu"]/li/div/span[normalize-space()="{menu}"]/ancestor::li/ul/li/a/span[normalize-space()="{submenu}"]/parent::*'.format(
                menu=menu, submenu=submenu)
            return self.page.find_element_by_xpath(xpath)

        def tab(self, name):
            """菜单标签"""

            xpath = '//div[@id="app"]//div[@role="tablist"]/div[contains(@class,"ant-tabs-nav-container")]//div[contains(@class,"ant-tabs-nav-scroll")]//div[@role="tab"]/div/span[normalize-space()="{name}"]'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def orderlist_tab(self):
            """订单列表标签"""

            name = '订单列表'
            return self.tab(name)

        @property
        def order_settings_tab(self):
            """订单设置标签"""

            name = '订单设置'
            return self.tab(name)

        @property
        def order_refund_tab(self):
            """订单退款标签"""

            name = '订单退款'
            return self.tab(name)

        @property
        def audit_tasklist_tab(self):
            """审核任务列表标签"""

            name = '审核任务列表'
            return self.tab(name)

        @property
        def cinema_audit_trail_tab(self):
            """影院审核跟踪标签"""

            name = '影院审核跟踪'
            return self.tab(name)

        @property
        def audit_settings_tab(self):
            """审核设置标签"""

            name = '审核设置'
            return self.tab(name)

    class Actions(BasePage.Actions):
        def home(self):
            """点击 左侧菜单 首页"""

            self.page.elements.home.click()
            return self

        def order(self, to_open=True):
            """点击 左侧菜单 订单"""

            self.page.open_or_shrink(self.page.elements.order, to_open)
            return self

        def order_manager(self, to_open=True):
            """点击 左侧子菜单 订单管理"""

            self.page.open_or_shrink(self.page.elements.order_manager, to_open)
            return self

        def order_list(self):
            """点击 左侧二级子菜单 订单列表"""

            self.page.elements.order_list.click()
            return self

        def order_settings(self):
            """点击 左侧二级子菜单 订单设置"""

            self.page.elements.order_settings.click()
            return self

        def order_refund(self, to_open=True):
            """点击 左侧子菜单 订单退款"""

            self.page.open_or_shrink(self.page.elements.order_refund, to_open)
            return self

        def data(self, to_open=True):
            """展开或者收缩 左侧菜单 数据"""

            self.page.open_or_shrink(self.page.elements.data, to_open)
            return self

        def userlist(self):
            """点击 左侧数据子菜单 用户列表"""

            self.page.elements.userlist.click()
            return self

        def labelrule(self):
            """点击 左侧数据子菜单 标签规则"""

            self.page.elements.labelrule.click()
            return self

        def adlist(self):
            """点击 左侧数据子菜单 广告片列表"""

            self.page.elements.adlist.click()
            return self

        def cinema_manage(self):
            """点击 左侧数据子菜单 影院管理"""

            self.page.elements.cinema_manage.click()
            return self

        def film_manage(self):
            """点击 左侧数据子菜单 影片管理"""

            self.page.elements.film_manage.click()
            return self

        def ad_place_manage(self):
            """点击 左侧数据子菜单 广告位管理"""

            self.page.elements.ad_place_manage.click()
            return self

        def audit(self, to_open=True):
            """点击 左侧菜单 审核"""

            self.page.open_or_shrink(self.page.elements.audit, to_open)
            return self

        def audit_tasklist(self):
            """点击 左侧子菜单 审核任务列表"""

            self.page.elements.audit_tasklist.click()
            return self

        def cinema_audit_trail(self):
            """点击 左侧子菜单 影院审核跟踪"""

            self.page.elements.cinema_audit_trail.click()
            return self

        def audit_settings(self):
            """点击 左侧子菜单 审核设置"""

            self.page.elements.audit_settings.click()
            return self

        def spread(self, to_open=True):
            """点击 左侧菜单 推广"""
            self.page.open_or_shrink(self.page.elements.spread, to_open)
            return self

        def haoyouzhuli(self):
            """点击 左侧子菜单 好友助力"""

            self.page.elements.haoyouzhuli.click()
            return self

        def orderlist_tab(self):
            """点击 订单列表标签"""

            self.page.elements.orderlist_tab.click()
            return self

        def order_refund_tab(self):
            """点击 订单退款标签"""

            self.page.elements.order_refund_tab.click()
            return self

        def audit_tasklist_tab(self):
            """点击 审核任务列表标签"""

            self.page.elements.audit_tasklist_tab.click()
            return self

        def cinema_audit_trail_tab(self):
            """点击 影院审核跟踪标签"""

            self.page.elements.cinema_audit_trail_tab.click()
            return self

        def audit_settings_tab(self):
            """点击 审核设置标签"""

            self.page.elements.audit_settings_tab.click()
            return self
