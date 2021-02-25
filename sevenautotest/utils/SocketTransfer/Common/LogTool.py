import logging


def logger(message, level=logging.DEBUG):
    logging.log(level=level, msg=message)
