import logging.config  # noqa: WPS301

from pricetransfer.settings import LOGGING


def get_my_logger(name):
    """Create logger."""
    logging.config.dictConfig(LOGGING)
    return logging.getLogger("testLogger.{0}".format(name))


def get_test_logger(name):
    """Create logger."""
    logging.config.dictConfig(LOGGING)
    return logging.getLogger("testLogger.{0}".format(name))
