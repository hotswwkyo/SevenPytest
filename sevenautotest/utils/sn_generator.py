# -*- coding:utf-8 -*-

import warnings

from .configmanager import ConfigManager


class SerialNumbersGenerator(object):

    INI = ConfigManager()
    DEFAULT_STEP = 1
    DEFAULT_LENGTH = 5
    DEFAULT_SECTION = 'SN'
    DEFAULT_OPTION = 'value'
    DEFAULT_START_NUMBER = 1

    def __init__(self, section=None, option=None, length=5, step=1, start_number=1):

        self.set_section(section)
        self.set_option(option)
        self.set_length(length)
        self.set_step(step)
        self.set_start_number(start_number)

    def set_section(self, section):

        if section and isinstance(section, str):
            self._section = section
        else:
            tips = 'section 必须是字符串，否则取默认值({}),实际传进来的值是: {}'.format(self.DEFAULT_SECTION, section)
            self._section = self.DEFAULT_SECTION
            warnings.warn(tips)
        return self

    @property
    def section(self):

        return self._section

    def set_option(self, option):

        if option and isinstance(option, str):
            self._option = option
        else:
            tips = 'option 必须是字符串，否则取默认值({}),实际传进来的值是: {}'.format(self.DEFAULT_OPTION, option)
            self._option = self.DEFAULT_OPTION
            warnings.warn(tips)
        return self

    @property
    def option(self):

        return self._option

    def set_length(self, length):

        if length and isinstance(length, int):
            self._length = length
        else:
            tips = 'length 必须是正整数，否则取默认值({}),实际传进来的值是: {}'.format(self.DEFAULT_LENGTH, length)
            self._length = self.DEFAULT_LENGTH
            warnings.warn(tips)
        return self

    @property
    def length(self):

        return self._length

    def set_step(self, step):

        if step and isinstance(step, int):
            self._step = step
        else:
            tips = 'step 必须是正整数，否则取默认值({}),实际传进来的值是: {}'.format(self.DEFAULT_STEP, step)
            self._step = self.DEFAULT_STEP
            warnings.warn(tips)
        return self

    @property
    def step(self):

        return self._step

    def set_start_number(self, start_number):

        if start_number and isinstance(start_number, int):
            self._start_number = start_number
        else:
            tips = 'start_number 必须是正整数，否则取默认值({}),实际传进来的section值是: {}'.format(self.DEFAULT_START_NUMBER, start_number)
            self._start_number = self.DEFAULT_START_NUMBER
            warnings.warn(tips)
        return self

    @property
    def start_number(self):

        return self._start_number

    @property
    def serial_numbers(self):

        used_sn = self.INI.get_with_lock(self.section, self.option)
        if used_sn:
            try:
                sn = int(used_sn) + self.step
            except Exception:
                sn = self.start_number
        else:
            sn = self.start_number
        self.INI.set_with_lock(self.section, self.option, str(sn))
        fmt_str = '{:>0%sd}' % self.length
        return fmt_str.format(sn)
