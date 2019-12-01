# SevenPytest
基于pytest实现，参考testng，定制测试用例收集方案和自定义参数化方案，使用pytest-html插件定制化html测试报告，采用page object设计模式，以及引入链式编程，语义清晰。自定义设计了测试用例数据以及页面元素定位数据存储方案。
## 一、页面封装
封装的页面需要继承根页面类放在pages库下，同时需要有两个内部类Elements（元素类）和Actions（动作类），分别用于封装页面的元素和页面动作。页面会自动实例化这两个类，分别赋给页面属性elements和actions。页面提供的元素查找方法与selenium相同。
    
* 页面元素类（Elements）需要继承自根页面元素类（BasePage.Elements），元素方法需要接受一个参数，使用装饰器（PageElementLocators）从元素定  位数据excel文件里读出数据会作为字典传给参数。装饰器（PageElementLocators）有两个参数file_name、file_dir_path。file_name元素定位器文件名，未指定则以页面类名作为文件名。file_dir_path元素定位器文件所在的目录路径，未指定则以settings.py配置文件的PAGE_ELEMENTS_LOCATORS_ROOT_DIR作为默认查找目录。元素定位数据在excel中格式定义如下：
	>* 元素方法定位器区域的第一行，第一列是区域分隔符（使用 页面元素定位器 进行分隔），第二列是元素方法名称，第三列是元素名称
	>* 元素方法定位器区域的第二行是数据标题
	>* 元素方法定位器区域的第三行是数据<br>
	> ![image locators](https://github.com/hotswwkyo/SevenPytest/raw/master/img/page_element_locators.png"元素定位器")
* 页面动作类（Actions）需要继承自根页面元素类（BasePage.Actions）,当前动作方法不需要返回数据处理时，可以考虑返回动作实例本身（self），在编写用例业务的时候就可以使用链式编程
<br>
* 示例：

```python
# -*- coding:utf-8 -*-

"""
登录页面示例
"""

import os
from uitest.pages import BasePage
from uitest.pages import PageElementLocators as page_element_locators

class LoginPage(BasePage):  
    
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
        def login(self, locators):
            """登录按钮"""          
            
            xpath = locators.get("登录")
            return self.page.find_element_by_xpath(xpath)
        
    class Actions(BasePage.Actions):
        
        def select_login_frame(self):
            """进入frame"""
            
            self.page.select_frame(self.page.elements.login_frame)
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

<br>
## 二、测试用例数据
测试用例数据存放excel文件中，文件名需以测试类名作为名称，统一放在主目录下的testdata目录下。数据在文件中以用例数据块的方式存储，数据块定义如下：
>* 所有行中的第一列是标记列，第一行第一列是数据块开始标记
>* 第一行: 用例名称信息(标记列的下一列是用例方法名称列，之后是用例名称列)
>* 第二行: 用例数据标题
>* 第三行 开始 每一行都是一组完整的测试数据直至遇见空行或者下一个数据块<br>
> ![image testdata](https://github.com/hotswwkyo/SevenPytest/raw/master/img/testcase_data_excel_file.png"测试用例数据")

## 三、用例编写
测试用例业务代码需要放在包uitest下的子包testcases下，编写规则如下：
>* 测试用例类需要继承抽象用例类（AbstractTestCase）
>* 测试方法需要使用标记pytest.mark.testcase进行标记，才会被当作测试用例进行收集，使用位置参数设置用例名，关键字参数author设置用例编        写者和editor设置最后修改者
>* 测试方法需要接收一个参数，参数化时从测试数据文件取出的该方法测试数据作为字典传给该测试方法

* 示例：

```python       
# -*- coding:utf-8 -*-

"""
登录页面测试示例
"""

import pytest
from uitest import settings
from uitest.testcases import AbstractTestCase
from uitest.pages.login import LoginPage

class LoginPageTest(AbstractTestCase):
    
    def setup_class(self):
        
        pass
        
    def setup_method(self):
        
        pass    
    
    @pytest.mark.testcase("成功登陆测试", author="siwenwei", editor="")
    def test_successfully_login(self, testdata):
        
        name    = testdata.get("用户名")
        pwd     = testdata.get("密码")
        url     = testdata.get("登录页面URL")
        
        page    = LoginPage()
        page.chrome(executable_path = settings.CHROME_DRIVER_PATH).maximize_window().open_url(url).actions.select_login_frame().sleep(1000).username(name).password(pwd).sleep(2000).login().sleep(3000)
        page.screenshot("successfully login.png")
        page.sleep(3000)
        
    def teardown_method(self):
        
        pass
        
    def teardown_class(self):
        
        self.BROWSER_MANAGER.close_all_browsers()
        
if __name__=="__main__":
    pass       
```

## 四、执行测试
    直接运行主目录下的TestRunner.py，也可以在命令行使用pytest命令执行
