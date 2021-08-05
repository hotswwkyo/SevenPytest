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
# from _pytest.compat import getimfunc
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

    cells.insert(0, html.th('用例名称', style="width:30%;"))
    cells.insert(1, html.th('用例数据', style="width:36%;"))
    # cells.insert(2, html.th('执行时间', class_='sortable time', col='time'))
    cells.insert(2, html.th('编写人', style="width:5%;"))
    cells.insert(3, html.th('修改人', style="width:5%;"))
    # cells.insert(1,html.th("Test_nodeid"))
    cells.pop()
    change_opts = {
        "Test": {
            "text": "用例方法",
            "style": "width: 10%;"
        },
        "Duration": {
            "text": "耗时",
            "style": "width:6%;"
        },
        "Result": {
            "text": "测试结果",
            "style": "width:10%;"
        },
    }
    for cell in cells:
        value = cell[0] if cell else ""
        if value in change_opts:
            details = change_opts[value]
            cell[0] = details["text"]
            skey = "style"
            if skey in details:
                add_style = details.get(skey, "")
                style = cell.attr.__dict__.get("style", "")
                if style:
                    cell.attr.__dict__.update(dict(style="{};{}".format(style.rstrip(";"), add_style)))
                else:
                    cell.attr.__dict__.update(dict(style=add_style))


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("日期: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))])
    for item in summary:
        if not item:
            continue
        text = item[0]
        if text == "(Un)check the boxes to filter the results.":
            item[0] = "(取消)勾选复选框，筛选显示测试结果。"
        elif 'tests ran in' in text:
            parts = text.split(" ")
            try:
                total = parts[0]
                seconds = parts[-3]
            except IndexError:
                pass
            else:
                item[0] = "执行了{}个测试用例，整个测试耗时：{}秒。".format(total, seconds)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):

    cells.insert(0, html.td(report.description if hasattr(report, "description") else ""))
    cells.insert(1, html.td(report.testdata if hasattr(report, "testdata") else ""))
    # cells.insert(2, html.td(datetime.now(), class_='col-time'))
    cells.insert(2, html.td(report.author if hasattr(report, "author") else ""))
    cells.insert(3, html.td(report.editor if hasattr(report, "editor") else ""))
    # cells.insert(1,html.td(report.nodeid))
    cells.pop()
    for cell in cells:
        value = cell[0] if cell else ""
        if value == report.nodeid:
            # cell[0] = report.nodeid.split("::")[-1]
            cell[0] = "..."
            cell.attr.__dict__.update(dict(title=report.nodeid, style="text-align: center;font-weight: bold;"))


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = item.function.__doc__ if item.function.__doc__ else item.function.__name__
    extra = getattr(report, 'extra', [])

    if report.when == "call":  # 测试用例失败自动截图

        # fill testdata
        args = {}
        for argname in item._fixtureinfo.argnames:
            args[argname] = item.funcargs[argname]
        setattr(report, "testdata", json.dumps(args, ensure_ascii=False))

        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            try:
                mm = item.cls.WECHAT_MANAGER
                if mm.native:
                    fp = mm.screenshot(report.description)
                    any([fp])
            except Exception as e:
                print(str(e))
            try:
                driver = item.cls.DRIVER_MANAGER.driver
            except NoOpenBrowser:
                driver = None
            capturer = ScreenshotCapturer(driver)
            # 不再保存失败截图 comment by siwenwei at 2021-08-04
            # file_name = report.description + ".png"
            # ss_result, ss_path = capturer.screenshot(file_name)
            img_base64 = capturer.screenshot_as_base64()
            if settings.ATTACH_SCREENSHOT_TO_HTML_REPORT:
                template = """<div><img src="data:image/png;base64,%s" alt="%s" style="width:600px;height:300px;" onclick="window.open(this.src)" align="right"/></div>"""
                # comment by siwenwei at 2021-08-04
                # html = template % (ScreenshotCapturer.screenshot_file_to_base64(ss_path) if ss_result else """<div>截图失败</div>""", "screenshot of test failure")
                html = template % (img_base64 if img_base64 else """<div>截图失败</div>""", "screenshot of test failure")
                extra.append(pytest_html.extras.html(html))

    report.extra = extra
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    for marker in item.iter_markers(settings.TESTCASE_MARKER_NAME):
        for k, v in marker.kwargs.items():
            setattr(report, k, v)


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers", "%s(name): Only used to set test case name to test method" % settings.TESTCASE_MARKER_NAME)
    config.addinivalue_line("testpaths", settings.TESTCASES_DIR)

    config.addinivalue_line("python_files", "*.py")
    config.addinivalue_line("filterwarnings", "ignore::UserWarning")

    opts = ["JAVA_HOME", "Packages", "Platform", "Plugins", "Python"]
    for opt in opts:
        config._metadata.pop(opt, None)


# def pytest_collect_file(path, parent):

# ext = path.ext
# bn  = path.basename
# pb  = path.purebasename
# if ext==".py" and bn != settings.PY_INIT_FILE_NAME:
# if not parent.session.isinitpath(path):
# for pat in parent.config.getini('python_files'):
# if path.fnmatch(pat):
# break
# else:
# if path.dirname == settings.TESTCASES_DIR or path.dirname.startswith(settings.TESTCASES_DIR):
# return parent.ihook.pytest_pycollect_makemodule(path=path, parent=parent)
# return
# return parent.ihook.pytest_pycollect_makemodule(path=path, parent=parent)


def pytest_pycollect_makeitem(collector, name, obj):
    """
    @see PyCollector._genfunctions
    @see _pytest.python
    """

    if safe_isclass(obj):
        if collector.istestclass(obj, name) or (issubclass(obj, AbstractTestCase) and obj != AbstractTestCase):
            return pytest.Class(name, parent=collector)
    else:
        obj = getattr(obj, "__func__", obj)
        if (inspect.isfunction(obj) or inspect.isfunction(get_real_func(obj))) and getattr(obj, "__test__", True) and isinstance(collector, pytest.Instance) and hasattr(obj, "pytestmark"):
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
    test_class_name = metafunc.cls.__name__
    test_method_name = metafunc.function.__name__
    testdata_file_path = os.path.join(settings.TEST_DATA_EXCEL_DIR, test_class_name + ".xlsx")

    this_case_datas = []
    testcases = TestCaseExcelFileReader(testdata_file_path).load_testcase_data()

    for testcase in testcases:

        if testcase.name == test_method_name:
            for row in testcase.datas:
                line = {}
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
        argname = ""
        this_case_datas = []
    elif len(argnames) < 2:
        argname = argnames[0]
    else:
        emf = "{funcname}() can only be at most one parameter, but multiple parameters are actually defined{args}"
        raise TypeError(emf.format(funcname=test_method_name, args=", ".join(argnames)))
    metafunc.parametrize(argname, this_case_datas)
