# -*- coding: utf-8 -*-
"""

"""

__version__ = "1.0"
__author__ = "si wen wei"

import sys
import pytest
from sevenautotest import settings


class TestRunner(object):
    def __init__(self):
        pass

    def run(self, args=None, plugins=None):
        """ return exit code, after performing an in-process test run.

        @param args:        list of command line arguments.

        @param plugins: list of plugin objects to be auto-registered during
                        initialization.
        @see pytest.main(list, list)
        """

        return pytest.main(args, plugins)


if __name__ == "__main__":

    if getattr(settings, "DEBUG", True):
        cmds = settings.PYTEST_COMMANDS
    else:
        cmds = sys.argv[1:]
    TestRunner().run(cmds)
