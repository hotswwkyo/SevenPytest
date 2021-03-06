# -*- coding: utf-8 -*-
"""
https://www.programcreek.com/python/example/81431/pytest.config
"""

__version__ = "1.0"
__author__ = "si wen wei"

import os
import json
import inspect
from datetime import datetime

import pytest
from py.xml import html
from _pytest.compat import getimfunc
from _pytest.compat import safe_isclass
from _pytest.compat import is_generator
from _pytest.compat import get_real_func

from sevenautotest import settings
from sevenautotest.exceptions import NoOpenBrowser
from sevenautotest.basetestcase import AbstractTestCase
from sevenautotest.reader import TestCaseExcelFileReader
from sevenautotest.utils.ScreenshotCapturer import ScreenshotCapturer

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    
    cells.insert(1, html.th('Description'))
    cells.insert(2, html.th('TestData'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    cells.insert(4, html.th('Author'))
    cells.insert(5, html.th('Editor'))
    # cells.insert(1,html.th("Test_nodeid"))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    
    cells.insert(1, html.td(report.description if hasattr(report, "description") else ""))
    cells.insert(2, html.td(report.testdata if hasattr(report, "testdata") else ""))
    cells.insert(3, html.td(datetime.utcnow(), class_='col-time'))
    cells.insert(4, html.td(report.author if hasattr(report, "author") else ""))
    cells.insert(5, html.td(report.editor if hasattr(report, "editor") else ""))
    # cells.insert(1,html.td(report.nodeid))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    
    pytest_html         = item.config.pluginmanager.getplugin('html')
    outcome             = yield
    report              = outcome.get_result()
    report.description  = item.function.__doc__ if item.function.__doc__ else item.function.__name__    
    extra               = getattr(report, 'extra', [])
    
    if report.when == "call": #测试用例失败自动截图
        
        # fill testdata
        args = {}
        for argname in item._fixtureinfo.argnames:
            args[argname] = item.funcargs[argname]
        setattr(report, "testdata", json.dumps(args, ensure_ascii=False))
        
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            try:
                driver = item.cls.DRIVER_MANAGER.driver
            except NoOpenBrowser:
                driver = None
            capturer            = ScreenshotCapturer(driver)
            file_name           = report.description+".png"
            ss_result, ss_path  = capturer.screenshot(file_name)
            if settings.ATTACH_SCREENSHOT_TO_HTML_REPORT:
                template    = """<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" onclick="window.open(this.src)" align="right"/></div>"""
                html        =  template % ScreenshotCapturer.screenshot_file_to_base64(ss_path) if ss_result else """<div>截图失败</div>"""
                extra.append(pytest_html.extras.html(html)) 
            
    report.extra    = extra
    report.nodeid   = report.nodeid.encode("utf-8").decode("unicode_escape")
    for marker in item.iter_markers(settings.TESTCASE_MARKER_NAME):
        for k, v in marker.kwargs.items():
            setattr(report, k, v)

def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "%s(name): Only used to set test case name to test method" % settings.TESTCASE_MARKER_NAME
    )
    config.addinivalue_line(
        "testpaths", settings.TESTCASES_DIR
    )
    
def pytest_collect_file(path, parent):
    
    ext = path.ext
    bn  = path.basename 
    pb  = path.purebasename
    
    if ext==".py" and bn != settings.PY_INIT_FILE_NAME:     
        if not parent.session.isinitpath(path):
            for pat in parent.config.getini('python_files'):
                if path.fnmatch(pat):
                    break
            else:
                if path.dirname == settings.TESTCASES_DIR or path.dirname.startswith(settings.TESTCASES_DIR):
                    return parent.ihook.pytest_pycollect_makemodule(path=path, parent=parent)
                return
        return parent.ihook.pytest_pycollect_makemodule(path=path, parent=parent)
    
def pytest_pycollect_makeitem(collector, name, obj):
    """
    @see PyCollector._genfunctions
    @see _pytest.python
    """ 
    
    if safe_isclass(obj) :
        if collector.istestclass(obj, name) or (issubclass(obj, AbstractTestCase) and obj !=AbstractTestCase):
            return pytest.Class(name, parent = collector)
    else:
        obj = getattr(obj, "__func__", obj)
        if (inspect.isfunction(obj) or inspect.isfunction(get_real_func(obj)))  and getattr(obj, "__test__", True) and isinstance(collector, pytest.Instance) and hasattr(obj, "pytestmark"):
            if not is_generator(obj):
                return list(collector._genfunctions(name, obj)) 
            else:
                return []
        else:
            return []
    # elif collector.istestfunction(obj, name):
        # return list(collector._genfunctions(name, obj))
    
def pytest_collection_modifyitems(session, config, items):
    
    new_items = []
    for item in items:
        if len(list(item.iter_markers(settings.TESTCASE_MARKER_NAME))):
            new_items.append(item)
            break
    items = new_items
    
def pytest_generate_tests(metafunc):
    
    for marker in metafunc.definition.iter_markers():
        if marker.name == settings.TESTCASE_MARKER_NAME:
            metafunc.function.__doc__ = "".join(marker.args)
            break
    test_class_name     = metafunc.cls.__name__
    test_method_name    = metafunc.function.__name__    
    testdata_file_path  = os.path.join(settings.TEST_DATA_EXCEL_DIR, test_class_name + ".xlsx")
    
    this_case_datas     = []
    testcases           = TestCaseExcelFileReader(testdata_file_path).load_testcase_data()

    for testcase in testcases:
        
        if testcase.name == test_method_name:
            for row in testcase.datas:
                line                = {}
                for cell in row:
                    for title, value in cell.items():
                        if title in line.keys():
                            continue
                        else:
                            line[title] = value
                this_case_datas.append(line)
            break
    # argnames = metafunc.funcargnames
    argnames = metafunc.definition._fixtureinfo.argnames
    
    if len(argnames) < 1:
        argname         = ""
        this_case_datas = []
    elif len(argnames) < 2:
        argname = argnames[0]
    else:
        emf = "{funcname}() can only be at most one parameter, but multiple parameters are actually defined{args}"
        raise TypeError(emf.format(funcname = test_method_name, args = ", ".join(argnames)))
    metafunc.parametrize(argname, this_case_datas)
    