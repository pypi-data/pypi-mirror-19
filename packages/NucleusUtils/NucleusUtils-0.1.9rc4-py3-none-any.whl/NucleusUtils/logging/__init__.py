import logging

from . import decorators
from . import dumps

handlers = []
log_level = logging.DEBUG


def set_level(level):
    global log_level
    log_level = level


def register_handler(handler):
    handlers.append(handler)


def get_logger(name='app'):
    """
    Get logger with handlers
    :param name: logger name
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(log_level)

    log_handlers = []
    for handler in logger.handlers:
        log_handlers.append(handler.__class__)

    for handler in handlers:
        if handler.__class__ not in log_handlers:
            logger.addHandler(handler)

    return logger
