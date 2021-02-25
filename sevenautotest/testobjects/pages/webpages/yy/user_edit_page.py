# -*- coding: utf-8 -*-

from sevenautotest.basepage import BasePage

__author__ = "si wen wei"


class UserEditPage(BasePage):
    """用户编辑页面"""
    @classmethod
    def join_two_xpath(cls, x1, x2):
        """拼接xpath"""

        slash = '/'
        if x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2[1:]
        elif not x1.endswith(slash) and x2.startswith(slash):
            return x1 + x2
        elif x1.endswith(slash) and not x2.startswith(slash):
            return x1 + x2
        else:
            return x1 + slash + x2

    @classmethod
    def join_xpath(cls, *xpath):

        first = xpath[0]
        others = xpath[1:]
        full_xpath = first
        for x in others:
            full_xpath = cls.join_two_xpath(full_xpath, x)
        return full_xpath

    class Elements(BasePage.Elements):
        @property
        def _user_baseinfo_form_xpath(self):

            xpath = '//div[@id="app"]/following-sibling::div/div[contains(@class,"ant-drawer")]/div[contains(@class,"ant-drawer-content-wrapper")]//div[contains(@class, "ant-drawer-body")]//div[contains(@class,"ant-card-body")]/form[contains(@class,"ant-form")]'
            return xpath

        @property
        def user_phone(self):
            """手机号码"""

            label = '手机号码'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="adjustNum"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        def _gender_radio(self, name):
            """性别 选项中的单选框"""

            label = '性别'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//label/span[normalize-space()="{name}"]/parent::*/span'.format(
                label=label, name=name)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def male_radio(self):
            """性别-男单选框"""

            name = '男'
            return self._gender_radio(name)

        @property
        def female_radio(self):
            """性别-女单选框"""

            name = '女'
            return self._gender_radio(name)

        def _user_lifecycle_radio(self, name):
            """用户生命周期标签单选框"""

            label = '用户生命周期标签'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label/span[contains(text(),"{label}")]/ancestor::div/following-sibling::div//label/span[normalize-space()="{name}"]/parent::*/span'.format(
                label=label, name=name)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def system_assignment_lifecycle(self):
            """用户生命周期标签 - 系统默认分配"""

            name = '系统默认分配'
            return self._user_lifecycle_radio(name)

        @property
        def import_period(self):
            """用户生命周期标签 - 导入期"""

            name = '导入期'
            return self._user_lifecycle_radio(name)

        @property
        def growth_period(self):
            """用户生命周期标签 - 成长期"""

            name = '成长期'
            return self._user_lifecycle_radio(name)

        @property
        def mature_period(self):
            """用户生命周期标签 - 成熟期"""

            name = '成熟期'
            return self._user_lifecycle_radio(name)

        @property
        def dormancy_period(self):
            """用户生命周期标签 - 休眠期"""

            name = '休眠期'
            return self._user_lifecycle_radio(name)

        @property
        def loss_period(self):
            """用户生命周期标签 - 流失期"""

            name = '流失期'
            return self._user_lifecycle_radio(name)

        def _user_special_radio(self, name):
            """用户特殊属性标签单选框"""

            label = '用户特殊属性标签'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label/span[contains(text(),"{label}")]/ancestor::div/following-sibling::div//label/span[normalize-space()="{name}"]/parent::*/span'.format(
                label=label, name=name)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def default_assignment_user(self):
            """用户特殊属性标签 - 系统默认分配"""

            name = '系统默认分配'
            return self._user_special_radio(name)

        @property
        def kol_user(self):
            """用户特殊属性标签 - KOL用户"""

            name = 'KOL用户'
            return self._user_special_radio(name)

        @property
        def active_user(self):
            """用户特殊属性标签 - 活跃用户"""

            name = '活跃用户'
            return self._user_special_radio(name)

        @property
        def sticky_user(self):
            """用户特殊属性标签 - 购买粘性用户"""

            name = '购买粘性用户'
            return self._user_special_radio(name)

        @property
        def high_unit_price_user(self):
            """用户特殊属性标签 - 高单价用户"""

            name = '高单价用户'
            return self._user_special_radio(name)

        @property
        def comeback_user(self):
            """用户特殊属性标签 - 回流用户"""

            name = '回流用户'
            return self._user_special_radio(name)

        def _user_kind_radio(self, name):
            """用户类型标签 选项中的单选框"""

            label = '用户类型标签'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//label/span[normalize-space()="{name}"]/parent::*/span'.format(
                label=label, name=name)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def merchant(self):
            """用户类型标签 - 商户"""

            name = '商户'
            return self._user_kind_radio(name)

        @property
        def personal(self):
            """用户类型标签 -  个人"""

            name = '个人'
            return self._user_kind_radio(name)

        @property
        def company_name(self):
            """企业运营昵称"""

            label = '企业运营昵称'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="compNickName"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def business_license_number(self):
            """营业执照编号"""

            label = '营业执照编号'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="compLicence"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def full_name(self):
            """姓名"""

            label = '姓名'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="realName"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def id_number(self):
            """身份证号"""

            label = '身份证号'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="idCard"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def belong_industry(self):
            """所属行业"""

            label = '所属行业'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//input[@id="belongIndustry"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def account_active_status(self):
            """账户启用状态"""

            label = '账户启用状态'
            xpath = 'div[contains(@class,"ant-form-item")]/div[contains(@class,"ant-form-item-label")]/label[normalize-space()="{label}"]/parent::*/following-sibling::div//button[@id="status"]'.format(
                label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

        @property
        def submit(self):
            """提交按钮"""

            label = '提 交'
            xpath = './following-sibling::div/button/span[normalize-space()="{label}"]/parent::*'.format(label=label)
            xpath = self.page.join_xpath(self._user_baseinfo_form_xpath, xpath)
            return self.page.find_element_by_xpath(xpath)

    class Actions(BasePage.Actions):
        def user_phone_equals(self, number):
            """检查手机号码"""

            n_text = self.page.elements.user_phone.text
            if n_text != number:
                self.page.fail('实际手机号码{}与预期{}不等'.format(n_text, number))
            return self

        def select_male(self):
            """性别 勾选 男"""

            self.page.elements.male_radio.click()
            return self

        def select_female(self):
            """性别 勾选 女"""

            self.page.elements.female_radio.click()
            return self

        def system_assignment_lifecycle(self):
            """点击 用户生命周期标签 - 系统默认分配"""

            self.page.elements.system_assignment_lifecycle.click()
            return self

        def click_import_period(self):
            """点击 用户生命周期标签 - 导入期"""

            self.page.elements.import_period.click()
            return self

        def click_growth_period(self):
            """点击 用户生命周期标签 - 成长期"""

            self.page.elements.growth_period.click()
            return self

        def click_mature_period(self):
            """点击 用户生命周期标签 - 成熟期"""

            self.page.elements.mature_period.click()
            return self

        def click_dormancy_period(self):
            """点击 用户生命周期标签 - 休眠期"""

            self.page.elements.dormancy_period.click()
            return self

        def click_loss_period(self):
            """点击 用户生命周期标签 - 流失期"""

            self.page.elements.loss_period.click()
            return self

        def default_assignment_user(self):
            """点击 用户特殊属性标签 -  系统默认分配"""

            self.page.elements.default_assignment_user.click()
            return self

        def kol_user(self):
            """点击 用户特殊属性标签 -  KOL用户"""

            self.page.elements.kol_user.click()
            return self

        def active_user(self):
            """点击 用户特殊属性标签 -  活跃用户"""

            self.page.elements.active_user.click()
            return self

        def sticky_user(self):
            """点击 用户特殊属性标签 -  购买粘性用户"""

            self.page.elements.sticky_user.click()
            return self

        def high_unit_price_user(self, expected):
            """点击 用户特殊属性标签 -  高单价用户"""

            self.page.elements.high_unit_price_user.click()
            return self

        def comeback_user(self, expected):
            """点击 用户特殊属性标签 -  回流用户"""

            self.page.elements.comeback_user.click()
            return self

        def merchant(self):
            """ 点击 用户类型标签 -  商户"""

            self.page.elements.merchant.click()
            return self

        def personal(self):
            """ 点击 用户类型标签 -  个人"""

            self.page.elements.personal.click()
            return self

        def select_usertype(self, usertype):

            if usertype == "个人":
                self.personal()
            elif usertype == "商户":
                self.merchant()
            else:
                pass
            return self

        def full_name(self, name):
            """输入姓名"""

            self.page.elements.full_name.clear()
            self.page.elements.full_name.send_keys(name)
            return self

        def id_number(self, number):
            """输入身份证号"""

            self.page.elements.id_number.clear()
            self.page.elements.id_number.send_keys(number)
            return self

        def belong_industry(self, name):
            """输入所属行业"""

            self.page.elements.belong_industry.clear()
            self.page.elements.belong_industry.send_keys(name)
            return self

        def click_account_active_status(self):
            """点击 账号启用状态"""

            self.page.elements.account_active_status.click()
            return self

        def company_name(self, name):
            """输入 企业运营昵称"""

            self.page.elements.company_name.clear()
            self.page.elements.company_name.send_keys(name)
            return self

        def business_license_number(self, number):
            """输入 营业执照编号"""

            self.page.elements.business_license_number.clear()
            self.page.elements.business_license_number.send_keys(number)
            return self

        def submit(self):
            """点击 提交按钮"""

            self.page.elements.submit.click()
            return self
