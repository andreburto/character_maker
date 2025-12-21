import logging
import sys


def get_logger(identifier):
    logger = logging.getLogger(identifier)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    return logger
