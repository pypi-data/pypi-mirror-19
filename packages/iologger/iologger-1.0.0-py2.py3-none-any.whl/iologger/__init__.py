"""
Decorator which logs the wrapped function/method.
The following are logged:
    1. The function called, it's args, and it's kwargs.
    2. The execution time of the function.
"""

import time
from functools import wraps

from logbook import Logger

__version__ = "1.0.0"


def iologger(function) -> None:
    """
    Decorator which logs the wrapped function/method.
    The following are logged:
        1. The function called, it's args, and it's kwargs.
        2. The execution time of the function.
    """

    logger = Logger("IOL - {}".format(
            function.__name__))

    @wraps(function)
    def wrapper(*args, **kwargs) -> None:
        logger.debug("Starting...")

        arg_dict = dict()
        arg_dict['args'] = args
        arg_dict['kwargs'] = kwargs
        logger.debug("args/kwargs = {}".format(arg_dict))

        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()

        logger.debug("Return Value: '{}'".format(result))
        logger.info("...Finished ({:0.3} seconds)".format(
                end - start))

        return result

    return wrapper
