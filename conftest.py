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
from sevenautotest.utils import helper

import pytest
from py.xml import html, raw
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
    cells.insert(4, html.th("开始时间"))
    cells.pop()
    change_opts = {
        "Test": {
            "text": "用例方法",
            "style": "width: 7%;"
        },
        "Duration": {
            "text": "耗时(秒)",
            "style": "width:9%;"
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

    style_css = 'table tr:hover {background-color: #f0f8ff;};'
    js = """
        function append(targentElement, newElement) {
            var parent = targentElement.parentNode;
            if (parent.lastChild == targentElement) {
                parent.appendChild(newElement);
            } else {
                parent.insertBefore(newElement, targentElement.nextSibling);
            }
        }
        function prettify_h2(){
            var h2list = document.getElementsByTagName("h2");
            var cnmaps = [['Environment', '环境'], ['Summary', '概要'], ['Results', '详情']];
            var env = cnmaps[0][0];
            var is_del_env_area = true;
            var env_indexs = [];
            for(var i=0;i<h2list.length;i++){
                var h2 = h2list[i];
                if(env == h2.innerText){
                    env_indexs.push(i);
                    if(!is_del_env_area){
                        append(h2, document.createElement('hr'));
                    }
                }else{
                    for(var s=0;s<cnmaps.length;s++){
                        var onemap = cnmaps[s];
                        if(h2.innerText == onemap[0]){
                            append(h2, document.createElement('hr'));
                            break;
                        }
                    }
                }
                h2.style.marginTop = "50px";
                for(var j=0;j<cnmaps.length;j++){
                    var one = cnmaps[j];
                    if(h2.innerText == one[0]){
                        h2.innerText = one[1];
                        break;
                    }
                }
            }
            if(!is_del_env_area){
                return;
            }
            for(var k=0;k<env_indexs.length;k++){
                var index = env_indexs[k];
                var h2 = h2list[index];
                var el_env = document.getElementById('environment');
                h2.parentNode.removeChild(h2);
                if(el_env){
                    el_env.parentNode.removeChild(el_env);
                }
            }
        }
        var event_func = document.body.onload;
        document.body.onload = function(){return false;};
        if (window.attachEvent) {
            window.attachEvent("onload", event_func);
            window.attachEvent("onload", prettify_h2);
        } else if (window.addEventListener) {
            window.addEventListener("load", event_func, false);
            window.addEventListener("load",prettify_h2, false);
        }
    """
    prefix.extend([html.style(raw(style_css))])
    prefix.extend([html.script(raw(js))])
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
                try:
                    seconds = helper.SevenTimeDelta(seconds=float(seconds)).human_readable()
                except Exception:
                    pass
                item[0] = "执行了{}个测试用例，整个测试耗时：{}".format(total, seconds)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):

    cells.insert(0, html.td(getattr(report, "description", "")))
    cells.insert(1, html.td(getattr(report, "testdata", "")))
    # cells.insert(2, html.td(datetime.now(), class_='col-time'))
    cells.insert(2, html.td(getattr(report, "author", "")))
    cells.insert(3, html.td(getattr(report, "editor", "")))
    cells.insert(4, html.td(getattr(report, "testcase_exec_start_time", "")))
    cells.pop()
    method_names = [report.nodeid]
    whenlist = ['setup', 'call', 'teardown']
    for when in whenlist:
        suffix = "::" + when
        if not report.nodeid.endswith(suffix):
            method_names.append(report.nodeid + suffix)
    copy_to_clipboard = "var transfer = document.createElement('input');this.appendChild(transfer);transfer.value = this.title;transfer.focus();transfer.select();if (document.execCommand('copy')) {document.execCommand('copy');};transfer.blur();this.removeChild(transfer);"
    for cell in cells:
        value = cell[0] if cell else ""
        if value in method_names:
            # cell[0] = report.nodeid.split("::")[-1]
            cell[0] = "..."
            cell.attr.__dict__.update(dict(title=value, style="text-align: center;font-weight: bold;", onclick=copy_to_clipboard))


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = item.function.__doc__ if item.function.__doc__ else item.function.__name__
    extra = getattr(report, 'extra', [])

    # fill testdata
    args = {}
    for argname in item._fixtureinfo.argnames:
        args[argname] = item.funcargs[argname]
    setattr(report, "testdata", json.dumps(args, ensure_ascii=False))

    if report.when == "call":  # 测试用例失败自动截图

        # comment the follow code at 2021-08-26 by siwenwei
        # fill testdata
        # args = {}
        # for argname in item._fixtureinfo.argnames:
        #     args[argname] = item.funcargs[argname]
        # setattr(report, "testdata", json.dumps(args, ensure_ascii=False))

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
    report.testcase_exec_start_time = getattr(item, "testcase_exec_start_time", "")


def pytest_addoption(parser):
    parser.addoption("--groups", action="store", help="run testcase which belong group name")


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
            if hasattr(pytest.Class, "from_parent"):
                return pytest.Class.from_parent(collector, name=name)
            else:
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


def enable_of_testcase_marker(testcase_markers):

    key = "enable"
    enable = False
    for m in testcase_markers:
        enable = m.kwargs.get(key, None)
        if enable is not None:
            break
    if enable is None:
        enable = True
    return enable


def get_group_name_from_nodeid(nodeid):
    sep = "::"
    parts = nodeid.split(sep)
    group_name = sep.join(parts[0:len(parts) - 1])
    return group_name


def priority_of_testcase_marker(testcase):

    key = "priority"
    markers = list(testcase.iter_markers(settings.TESTCASE_MARKER_NAME))
    priority = None  # 表示没有设置该priority参数
    for m in markers:
        priority = m.kwargs.get(key, None)
        if priority is not None:
            break
    return priority


def sorted_by_priority(testcases):
    """根据priority（优先级）对用例进行排序，如果没有设置priority，则不会对该用例进行排序，它的执行顺序不变"""

    groupnames = []
    for testcase in testcases:
        gname = get_group_name_from_nodeid(testcase.nodeid)
        if gname not in groupnames:
            groupnames.append(gname)

    groups = {}
    for gn in groupnames:
        group = []
        for i, tc in enumerate(testcases):
            if gn == get_group_name_from_nodeid(tc.nodeid) and priority_of_testcase_marker(tc) is not None:
                group.append((i, tc))

        group.sort(key=lambda x: x[0])  # 按照其在原用例列表中的位置进行排序
        new_group = sorted(group, key=lambda x: priority_of_testcase_marker(x[1]))  # 返回按照优先级进行排序的新列表

        itemlist = []
        for index, item in enumerate(new_group):
            new_index = group[index][0]  # 当前用例新的索引位置
            old_index = item[0]  # 当前用例原来的索引位置
            current_testcase = item[1]  # 当前用例
            itemlist.append((new_index, old_index, current_testcase))
        groups[gn] = itemlist

    for items in groups.values():
        for item in items:
            new_index = item[0]
            thiscase = item[2]
            testcases[new_index] = thiscase


def filter_by_groups(items, config):

    gvalue = config.getoption('groups')
    groups = gvalue.split() if isinstance(gvalue, str) else []
    if groups:
        new_items = []
        for item in items:
            markers = list(item.iter_markers(settings.TESTCASE_MARKER_NAME))
            tc_groups = []
            for m in markers:
                mgroups = m.kwargs.get('groups', [])
                for mg in mgroups:
                    if mg not in tc_groups:
                        tc_groups.append(mg)
            for tcg in tc_groups:
                if tcg in groups:
                    new_items.append(item)
                    break
        items[:] = new_items


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):

    new_items = []
    for item in items:
        markers = list(item.iter_markers(settings.TESTCASE_MARKER_NAME))
        if len(markers) and enable_of_testcase_marker(markers):
            new_items.append(item)
    sorted_by_priority(new_items)
    items[:] = new_items
    filter_by_groups(items, config)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    item.testcase_exec_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


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
