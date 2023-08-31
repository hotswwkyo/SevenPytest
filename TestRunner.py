# -*- coding: utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

# import io
# import sys
import argparse
import pytest
from sevenautotest import settings

# 解决测试报告没有错误日志的问题：是因为这条代码导致传pytest命令行参数--capture 时报错导致无法捕获日志
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


class TestRunner(object):

    CMD_MODEL_ARG_NAME = '-cmdmode'

    def __init__(self):

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(self.CMD_MODEL_ARG_NAME, action="store_true", help="控制是否从命令行获取pytest运行参数")

        known_args, unknown_args = self.parser.parse_known_args()
        self.cmd_args = (known_args, unknown_args)

    @property
    def cmdmode(self):

        return self.cmd_args[0].cmdmode

    @property
    def pytest_args_from_cmd_line(self):
        """当从命令行获取pytest运行参数时，命令行没有设置以下参数时，自动获取settings.py配置文件中的对应设置，自动加入到命令行中

        useage: python TestRunner.py  -s -v -cmdmode sevenautotest\testcases\vncviewer_page_test.py
        """

        args = self.cmd_args[1].copy()
        parser = argparse.ArgumentParser()
        parser.add_argument("--html", help="html report file path")
        parser.add_argument("--junit-xml", dest="junit_xml", help="junit xml report file path")
        parser.add_argument("--self-contained-html", dest="self_contained_html", help="Run tests in headed mode.")
        parser.add_argument("--capture", help="per-test capturing method: one of fd|sys|no|tee-sys.")

        known_args, unknown_args = parser.parse_known_args(args)
        if known_args.capture is None:
            args.append('--capture=sys')
        if known_args.html is None:
            args.append('--html={}'.format(settings.HTML_REPORT_FILE_PATH))
        if known_args.junit_xml is None:
            args.append('--junit-xml={}'.format(settings.XML_REPORT_FILE_PATH))
        if known_args.self_contained_html is None:
            args.append('--self-contained-html')
        return args

    def run(self, args=None, plugins=None, mode='auto'):
        """ return exit code, after performing an in-process test run.

        @param args:        list of command line arguments.

        @param plugins: list of plugin objects to be auto-registered during
                        initialization.
        @see pytest.main(list, list)
        """
        mode = mode.lower()
        if mode == 'cmdline' or (mode == 'auto' and self.cmdmode):
            args = self.pytest_args_from_cmd_line
        return pytest.main(args, plugins)


if __name__ == "__main__":

    TestRunner().run(settings.PYTEST_COMMANDS)
