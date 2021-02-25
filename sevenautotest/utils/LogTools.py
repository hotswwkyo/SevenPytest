import logging
import threading


def logger(msg, level=logging.DEBUG):
    extra_dict = {"thread_name": threading.currentThread().name}
    logging.log(level=level, msg=msg, extra=extra_dict)
