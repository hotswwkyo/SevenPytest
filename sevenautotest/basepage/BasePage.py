# -*- coding:utf-8 -*-

"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

from . import AbstractBasePage
from sevenautotest import settings
from sevenautotest.manager import DriverManager

class BasePage(AbstractBasePage):
    """ """
    
    def init(self):
        
        pass
        
    def chrome(self, url=None, alias=None, *args, **kwargs):
        
        executable_path_key = "executable_path"
        if executable_path_key not in kwargs.keys():
            if hasattr(settings,"CHROME_DRIVER_PATH") and settings.CHROME_DRIVER_PATH and isinstance(settings.CHROME_DRIVER_PATH, str):
                kwargs[executable_path_key] = settings.CHROME_DRIVER_PATH
        return self.open_browser( DriverManager.CHROME_NAME, url, alias, *args, **kwargs)
 
if __name__ == "__main__":
    pass