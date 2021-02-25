# -*- coding:utf-8 -*-

from sevenautotest.basepage.base_minium_page import BaseMiniumPage


class ConfirmOrderPage(BaseMiniumPage):
    """ 确认订单页面 """
    class Elements(BaseMiniumPage.Elements):
        @property
        def total_amount(self):
            """合计金额"""

            selector = 'view.pay-bottom>view.pay-content>view.pay-price.text'
            el_texts = self.page.get_elements(selector)
            return el_texts[1]

        @property
        def submit(self):
            """提交订单按钮"""

            selector = 'view.pay-bottom>view.pay-content>view.pay-btn.text'
            inner_text = '提交订单'
            return self.page.get_element(selector, inner_text=inner_text)

    class Actions(BaseMiniumPage.Actions):
        def total_amount_equals(self, total, prefix='￥:'):
            """检查合计金额是否正确"""

            ttext = self.page.elements.total_amount.inner_text
            a_total = ttext.strip().lstrip(prefix)
            if a_total != total:
                self.page.fail('合计订单金额({})不等于预期({})'.format(a_total, total))
            return self

        def submit(self):
            """点击提交订单按钮"""

            self.page.elements.submit.click()
            return self
