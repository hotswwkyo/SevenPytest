# -*- coding:utf-8 -*-
'''
Created on 2020年6月10日

@author: siwenwei
'''
import os
import threading
import configparser

from sevenautotest import settings


class ConfigManager(object):
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.lock = threading.Lock()
        self.ini_file_name = settings.INI_FILE_NAME
        self.config.read(self.ini_file_path, encoding="utf-8")

    @property
    def ini_file_name(self):
        return self.__ini_file_name

    @ini_file_name.setter
    def ini_file_name(self, file_name):

        if isinstance(file_name, str):
            if file_name.endswith(".ini"):
                self.__ini_file_name = file_name
            else:
                self.__ini_file_name = file_name + ".ini"
        else:
            raise TypeError()

    @property
    def ini_file_path(self):

        return os.path.join(self.ini_file_dir_path, self.ini_file_name)

    @property
    def ini_file_dir_path(self):

        if not os.path.exists(settings.INI_FILE_DIR_PATH):
            os.mkdir(settings.INI_FILE_DIR_PATH)
        return settings.INI_FILE_DIR_PATH

    @property
    def ini_file_is_exists(self):
        return os.path.exists(self.ini_file_path)

    def set(self, section, option, value):

        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        return self

    def get(self, section, option, default=None):

        if self.config.has_option(section, option):
            return self.config.get(section, option)
        else:
            return default

    def write(self):

        with open(self.ini_file_path, "w+") as f:
            self.config.write(f)

    def get_with_lock(self, section, option, default=None):

        value = default
        with self.lock:
            value = self.get(section, option, default=default)
        return value

    def set_with_lock(self, section, option, value):

        with self.lock:
            self.update_if_change(section, option, value)
        return self

    def update_if_change(self, section, option, value):

        if self.get(section, option) != value:
            self.set(section, option, value)
            self.write()
