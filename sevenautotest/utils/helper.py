# -*- coding:utf-8 -*-

"""
通用功能
"""

import re
import inspect
import tkinter
import functools
from functools import cmp_to_key
import tkinter.simpledialog
from . import typetools

__version__ = "1.0"
__author__ = "si wen wei"

def is_positive_integer(value):
    
    return isinstance(value, int) and value >= 0

def is_empty_string(value):
    
    return typetools.is_string(value) and value == ""
    
def is_blank_space(value):
    
    return typetools.is_string(value) and value.strip() == ""
    
def group_by_suffix_regex(string_key_dict, suffix_regex, is_remove_suffix=True, cmp=None):
    """根据键名正则表达式对字典进行分组和排序
    
    @param string_key_dict 键名是字符串的字典
    @param suffix_regex 键名正则表达式
    @param is_remove_suffix 是否移除匹配的后缀
    @param cmp 如果是函数，会往cmp传入匹配的后缀，函数要求同sorted方法的cmp参数说明，如果是为True则按照匹配的后缀排序，False则不排序
    @return 返回分组后组构成的列表，每个组是一个字典 [group, group, ...]
    """
    
    regex   = "(.)*" + "(" + suffix_regex + ")"
    pattern = re.compile(regex)
    
    unique_suffixes     = []
    suffix_key_val_maps = []
    for k, v in string_key_dict.items():
        matcher = pattern.search(k)
        if matcher:
            full_key_name   = matcher.group(0)
            key_name_suffix = matcher.group(2)
            suffix_key_val_maps.append((key_name_suffix, full_key_name, v))
            if key_name_suffix not in unique_suffixes:
                unique_suffixes.append(key_name_suffix)
    
    # sorted
    if inspect.isfunction(cmp):
        unique_suffixes = sorted(unique_suffixes, key = cmp_to_key(cmp))
    elif cmp:
        unique_suffixes = sorted(unique_suffixes)
    
    # group
    groups = []
    for us in unique_suffixes:
        group = {}
        for suffix, key, val in suffix_key_val_maps:
            if us == suffix:
                if is_remove_suffix:
                    k = key[:len(key)-len(suffix)]
                else:
                    k = key
                group[k] = val
        if group:
            groups.append(group)            
    return groups

def digital_extractor(extractor=None):
    """数字提取函数装饰器,把被装饰的函数变成符合sorted要求的cmp函数
    
    @param extractor 数字提取函数 需要接受一个字符串参数，从中提取数字并返回
    """
    def wapper(func):
        @functools.wraps(func)
        def recv_args(suffix1, suffix2):
            return func(suffix1, suffix2, extractor)
        return recv_args        
    return wapper
    
@digital_extractor()
def digital_suffix_cmp(suffix1, suffix2, digital_extractor = None):
    """数字后缀比较器
    
    @param suffix1 以数字结尾的字符串1
    @param suffix2 以数字结尾的字符串2
    @param digital_extractor 数字提取函数 需要接受一个字符串参数，从中提取数字并返回
    """
    
    def _digital_extractor(suffix):
        regex   = "(\\d+)$"
        pattern = re.compile(regex)
        matcher = pattern.search(suffix)
        if not matcher:
            message = "所给的后缀" + "(" + suffix + ")" + "没有以数字结尾"
            raise ValueError(message)
        return matcher.group(1)
    
    if digital_extractor and inspect.isfunction(digital_extractor):
        extractor = digital_extractor
    else:
        extractor = _digital_extractor
        
    n1 = int(extractor(suffix1))
    n2 = int(extractor(suffix2))
    
    if n1 > n2:
        return 1
    elif n1 == n2:
        return 0
    else:
        return -1
        
def prompt(title = "",tips = "",encoding = "utf-8"):
    """用于显示可提示用户进行输入的对话框
    
    @param title 对话框标题
    @param tips 要在对话框中显示的文本
    """
    
    root            = Tkinter.Tk()  
    screen_width    = root.winfo_screenwidth()
    screen_height   = root.winfo_screenheight() - 100    #under windows, taskbar may lie under the screen
    root.resizable(False,False)
    root.withdraw()
    #移到屏幕外，避免闪烁
    root.geometry('+%d+%d' % (screen_width+100, screen_height+100))
    root.update_idletasks()
    # root.deiconify()    #now window size was calculated
    # root.withdraw()     #hide window again
    root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width())/2, (screen_height - root.winfo_height())/2) )    #center window on desktop
    root.update()
    root.withdraw()

    # root.deiconify()
    #add some widgets to the root window
    if not isinstance(title,unicode):
        title = title.decode(encoding)
    if not isinstance(tips,unicode):
        tips = tips.decode(encoding)
    value = tkinter.simpledialog.askstring(title, tips)
    if value==None:
        value = ""  
    return value
    
def escape_xpath_value(value):
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value
    
class DictToObject(object):
    def __init__(self, py_dict):
        """
        
        """
        if not isinstance(py_dict,dict):
            raise ValueError("Data Type Must Be dict")
        for field in py_dict:
            value = py_dict[field]
            if not isinstance(value,(dict,list)):
                setattr(self,"%s" % field,value)
            else:
                if isinstance(value,dict):
                    setattr(self,"%s" % field,self.__class__(value))
                else :
                    setattr(self,"%s" % field,self.analyze_list(value))
    def analyze_list(self,array):
        for index,value in enumerate(array):
            if isinstance(value,list):
                self.analyze_list(value)
            elif isinstance(value,dict): #if element of list is dict,converts the value of the element in the list into the object
                array[index] = self.__class__(value)
            else:
                pass
        return array
        
def get_the_number_of_pages(total_data, limit_size):
    """根据数据总数和每页显示数据数计算分页数
    
    @param total_data 数据总数
    @param limit_size 每页显示数据条数
    """
    quotient, remainder = divmod(total_data, limit_size)
    if remainder>0:
        quotient = quotient +1
    return quotient
    
def cutout_prefix_digital(string):
    
    regex = "^(\\d+)\\.*"
    pattern = re.compile(regex)
    matcher = pattern.search(string)
    if matcher:
        return matcher.group(1)
    else:
        return None