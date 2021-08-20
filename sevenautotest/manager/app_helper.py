#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: 思文伟
@Date: 2021/08/19
'''

import subprocess


class WinAppDriverHelper(object):
    def __init__(self):
        self.process = None
        self.executable_path = None

    def startup_winappdriver(self, executable_path, output_stream=None, auto_close_output_stream=False):
        """启动WinAppDriver.exe"""

        self.executable_path = executable_path
        try:
            # output_stream = open(os.devnull, 'w')
            self.process = subprocess.Popen([executable_path], stdout=output_stream)
        except Exception:
            self.process = None
        finally:
            if auto_close_output_stream and output_stream is not None:
                output_stream.close()

    def shutdown_winappdriver(self):
        """关闭WinAppDriver.exe"""

        from psutil import Process, NoSuchProcess
        try:
            process = Process(self.process.pid)
            for pro in process.children(recursive=True):
                pro.kill()
                pro.wait()
            self.process.kill()
            self.process.wait()
            self.process = None
        except (NoSuchProcess, AttributeError):
            subprocess.call("C:/Windows/system32/taskkill.exe /f /im WinAppDriver.exe", shell=False)
            self.process = None
