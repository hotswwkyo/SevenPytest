# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class AuditTaskListPage(BasePage):
    """雨燕管理后台审核任务列表页面"""
    class Elements(BasePage.Elements):
        def tab(self, name):
            """标签"""

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-tabs-nav-scroll")]//div[@role="tab" and contains(text(),"{name}")]'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def all_audit_tasks(self):
            """全部审核任务标签"""

            name = '全部审核任务'
            return self.tab(name)

        @property
        def to_be_audit(self):
            """待审核标签"""

            name = '待审核'
            return self.tab(name)

        @property
        def audit_pass(self):
            """审核通过标签"""

            name = '审核通过'
            return self.tab(name)

        @property
        def audit_fail(self):
            """审核未通过标签"""

            name = '审核未通过'
            return self.tab(name)

        @property
        def film_limit(self):
            """影片限制标签"""

            name = '影片限制'
            return self.tab(name)

        @property
        def unaudit_expire(self):
            """过期未审核标签"""

            name = '过期未审核'
            return self.tab(name)

        def _search_form_input(self, label):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        @property
        def audit_tasknumber(self):
            """审核任务编号输入框"""

            label = '审核任务编号'
            return self._search_form_input(label)

        @property
        def ad_number(self):
            """广告编号输入框"""

            label = '广告编号'
            return self._search_form_input(label)

        @property
        def time_to_first_run(self):
            """距首次执行时间 选择框"""

            label = '距首次执行时间'
            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//div[@role="combobox"]'.format(
                label=label)
            return self.page.find_element_by_xpath(xpath)

        def dropdown_selectlist(self, opt):
            """下拉列表选择框"""

            xpath = '//div[@id="app"]/following-sibling::div//div[contains(@class,"ant-select-dropdown")]/div[@id]/ul/li[@role="option" and normalize-space()="{opt}"]'.format(opt=opt)
            return self.page.find_element_by_xpath(xpath)

        def _search_form_button(self, name):

            xpath = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"table-page-search-wrapper")]/form//span[contains(@class,"table-page-search-submitButtons")]//button/span[normalize-space()="{name}"]/parent::*'.format(
                name=name)
            return self.page.find_element_by_xpath(xpath)

        @property
        def search_btn(self):
            """查询按钮"""

            return self._search_form_button('查 询')

        @property
        def reset_btn(self):
            """重置按钮"""

            return self._search_form_button('重 置')

        def table_row_checkbox(self, rowinfo, match_more=False):
            """ 根据条件 查找指定行，返回行的复选框元素

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    taskno: 审核任务编号
                    adno: 广告编号
                    orderno: 订单数量
                    filmno: 影片数量
                    status: 审核状态
                match_more: 是否返回匹配的多个的复选框 False --- 只返回匹配的第一个
            """
            checkbox_index = 1
            taskno_index = 2
            adno_index = 3
            orderno_index = 4
            filmno_index = 5
            status_index = 9

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-body")]/table/tbody/tr/'

            checkbox_col = 'td[{index}]/span'.format(index=checkbox_index)
            taskno_col = 'td[position()={index} and normalize-space()="{taskno}"]'
            adno_col = 'td[position()={index}]/div/a[normalize-space()="{adno}"]/parent::div/parent::td'
            orderno_col = 'td[position()={index} and normalize-space()="{orderno}"]'
            filmno_col = 'td[position()={index} and normalize-space()="{filmno}"]'
            status_col = 'td[position()={index}]/div/span[normalize-space()="{status}"]/parent::div/parent::td'

            taskno_k = 'taskno'
            adno_k = 'adno'
            orderno_k = 'orderno'
            filmno_k = 'filmno'
            status_k = 'status'

            valid_keys = [taskno_k, adno_k, orderno_k, filmno_k, status_k]

            has_vaild_key = False
            for k in valid_keys:
                if k in rowinfo.keys():
                    has_vaild_key = True
                    break
            if not has_vaild_key:
                raise KeyError('没有以下任意键：' + ", ".join(valid_keys))
            cols = []
            if taskno_k in rowinfo:
                cxpath = taskno_col.format(index=taskno_index, taskno=rowinfo[taskno_k])
                cols.append(cxpath)

            if adno_k in rowinfo:
                cxpath = adno_col.format(index=adno_index, adno=rowinfo[adno_k])
                cols.append(cxpath)

            if orderno_k in rowinfo:
                cxpath = orderno_col.format(index=orderno_index, orderno=rowinfo[orderno_k])
                cols.append(cxpath)

            if filmno_k in rowinfo:
                cxpath = filmno_col.format(index=filmno_index, filmno=rowinfo[filmno_k])
                cols.append(cxpath)

            if status_k in rowinfo:
                cxpath = status_col.format(index=status_index, status=rowinfo[status_k])
                cols.append(cxpath)
            cols.append(checkbox_col)

            xpath_body = "/parent::tr/".join(cols)
            full_xpath = xpath_header + xpath_body
            if match_more:
                return self.page.find_elements_by_xpath(full_xpath)
            else:
                return self.page.find_element_by_xpath(full_xpath)

        def _table_row_button(self, name, rowinfo):
            """ 根据条件 查找指定行内的按钮，并返回

            Args:
                name: 按钮名称
                rowinfo: 表格中行的列信息，键定义如下
                    taskno: 审核任务编号
                    adno: 广告编号
                    orderno: 订单数量
                    filmno: 影片数量
                    status: 审核状态
            """
            # btn_index = 1
            taskno_index = 2
            adno_index = 3
            orderno_index = 4
            filmno_index = 5
            status_index = 9

            xpath_header = '//div[@id="app"]//div[contains(@class,"ant-layout-content")]/div/div[contains(@class,"main")]//div[contains(@class,"ant-card-body")]//div[contains(@class,"ant-table-body")]/table/tbody/tr/'

            # btn_col = 'td[{index}]/span'.format(index=btn_index)
            btn_col = 'td/div/button/span[normalize-space()="{name}"]'.format(name=name)
            taskno_col = 'td[position()={index} and normalize-space()="{taskno}"]'
            adno_col = 'td[position()={index}]/div/a[normalize-space()="{adno}"]/parent::div/parent::td'
            orderno_col = 'td[position()={index} and normalize-space()="{orderno}"]'
            filmno_col = 'td[position()={index} and normalize-space()="{filmno}"]'
            status_col = 'td[position()={index}]/div/span[normalize-space()="{status}"]/parent::div/parent::td'

            taskno_k = 'taskno'
            adno_k = 'adno'
            orderno_k = 'orderno'
            filmno_k = 'filmno'
            status_k = 'status'

            valid_keys = [taskno_k, adno_k, orderno_k, filmno_k, status_k]

            has_vaild_key = False
            for k in valid_keys:
                if k in rowinfo.keys():
                    has_vaild_key = True
                    break
            if not has_vaild_key:
                raise KeyError('没有以下任意键：' + ", ".join(valid_keys))
            cols = []
            if taskno_k in rowinfo:
                cxpath = taskno_col.format(index=taskno_index, taskno=rowinfo[taskno_k])
                cols.append(cxpath)

            if adno_k in rowinfo:
                cxpath = adno_col.format(index=adno_index, adno=rowinfo[adno_k])
                cols.append(cxpath)

            if orderno_k in rowinfo:
                cxpath = orderno_col.format(index=orderno_index, orderno=rowinfo[orderno_k])
                cols.append(cxpath)

            if filmno_k in rowinfo:
                cxpath = filmno_col.format(index=filmno_index, filmno=rowinfo[filmno_k])
                cols.append(cxpath)

            if status_k in rowinfo:
                cxpath = status_col.format(index=status_index, status=rowinfo[status_k])
                cols.append(cxpath)
            cols.append(btn_col)

            xpath_body = "/parent::tr/".join(cols)
            full_xpath = xpath_header + xpath_body
            return self.page.find_element_by_xpath(full_xpath)

        def audit_btn(self, rowinfo):
            """审核按钮"""

            name = "审 核"
            return self._table_row_button(name, rowinfo)

        def audit_record_btn(self, rowinfo):
            """审核记录按钮"""

            name = "审核记录"
            return self._table_row_button(name, rowinfo)

    class Actions(BasePage.Actions):
        def all_audit_tasks(self):
            """点击 全部审核任务标签"""

            self.page.elements.all_audit_tasks.click()
            return self

        def to_be_audit(self):
            """点击 待审核标签"""

            self.page.elements.to_be_audit.click()
            return self

        def audit_pass(self):
            """点击 审核通过标签"""

            self.page.elements.audit_pass.click()
            return self

        def audit_fail(self):
            """点击 审核未通过标签"""

            self.page.elements.audit_fail.click()
            return self

        def film_limit(self):
            """点击 影片限制标签"""

            self.page.elements.film_limit.click()
            return self

        def unaudit_expire(self):
            """点击 过期未审核标签"""

            self.page.elements.unaudit_expire.click()
            return self

        def audit_tasknumber(self, taskno):
            """输入任务编号"""

            self.page.elements.audit_tasknumber.clear()
            self.page.elements.audit_tasknumber.send_keys(taskno)
            return self

        def ad_number(self, adno):
            """输入广告编号"""

            self.page.elements.ad_number.clear()
            self.page.elements.ad_number.send_keys(adno)
            return self

        def select_time(self, time):
            """选择 距首次执行时间"""

            self.page.elements.time_to_first_run.click()
            self.sleep(2)
            self.page.elements.dropdown_selectlist(time).click()
            return self

        def search(self):
            """点击 查询按钮"""

            self.page.elements.search_btn.click()
            return self

        def reset(self):
            """点击 重置按钮"""

            self.page.elements.reset_btn.click()
            return self

        def click_row(self, rowinfo, match_more=False):
            """根据条件 点击表格中的行的复选框

            Args:
                rowinfo: 表格中行的列信息，键定义如下
                    taskno: 审核任务编号
                    adno: 广告编号
                    orderno: 订单数量
                    filmno: 影片数量
                    status: 审核状态
                match_more: see self.page.elements.table_row_checkbox
            """
            cbs = self.page.elements.table_row_checkbox(rowinfo, match_more=match_more)
            if match_more:
                for cb in cbs:
                    cb.click()
            else:
                cbs.click()
            return self

        def audit(self, rowinfo):
            """点击 审核按钮"""

            self.page.elements.audit_btn(rowinfo).click()
            return self

        def audit_record(self, rowinfo):
            """点击 审核记录按钮"""

            self.page.elements.audit_record_btn(rowinfo).click()
            return self
