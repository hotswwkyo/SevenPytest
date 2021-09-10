# -*- coding: utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

import io
import sys
import argparse
import pytest
from sevenautotest import settings

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


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

        return self.cmd_args[1].copy()

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
