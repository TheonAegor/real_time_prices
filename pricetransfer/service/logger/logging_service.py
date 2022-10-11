import logging.config

from pricetransfer.settings import LOGGING


def get_my_logger(name):
    logging.config.dictConfig(LOGGING)
    # return logging.getLogger(f'mylogger.{name}')
    return logging.getLogger(f"testLogger.{name}")


def get_test_logger(name):
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(f"testLogger.{name}")
