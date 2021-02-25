# -*- coding: utf-8 -*-
'''
Created on 2020年6月21日

@author: siwenwei
'''

import os
import logging.config

from sevenautotest import settings
from sevenautotest.utils import logconfig


class Log(object):

    DEV = "dev"
    DEFAULT = ""
    SEVENTESTER = "seventester"

    @classmethod
    def load_log_config(cls):

        if not os.path.exists(settings.LOG_DIR_PATH):
            os.mkdir(settings.LOG_DIR_PATH)

        logging.config.dictConfig(logconfig.LOG_CONFG)

    @classmethod
    def get_logger(cls, name=None):

        if name:
            logger = logging.getLogger(name)
        else:
            logger = logging.getLogger(__name__)
        return logger


Log.load_log_config()
