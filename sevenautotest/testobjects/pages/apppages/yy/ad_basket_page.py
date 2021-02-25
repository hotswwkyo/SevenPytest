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
