"""Logging functions for page-loader."""

import logging

NONE = 'none'
INFO = 'info'  # noqa: WPS110
WARNING = 'warning'
DEBUG = 'debug'
LOG_MESSAGE_TEMPLATE = '%(asctime)s %(levelname)s:\t%(message)s'  # noqa:WPS323
LOG_TIME_TEMPLATE = '%H:%M:%S'


def setup(log_level):
    """Start logging with the specified level of details."""
    logger = logging.getLogger()
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        LOG_MESSAGE_TEMPLATE,  # noqa: WPS323
        LOG_TIME_TEMPLATE,
    )
    console.setFormatter(formatter)
    if log_level == NONE:
        level = logging.ERROR
    if log_level == INFO:
        level = logging.INFO
    elif log_level == WARNING:
        level = logging.WARNING
    elif log_level == DEBUG:
        level = logging.DEBUG
    logger.setLevel(level)
    logger.addHandler(console)
