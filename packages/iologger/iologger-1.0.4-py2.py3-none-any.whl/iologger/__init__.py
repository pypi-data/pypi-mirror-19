"""
Decorator which logs the wrapped function/method.

The following are logged:
    1. name of the function called
    2. arg(s) passed for the function called (if any)
    3. kwarg(s) passed for the function called (if any)
    4. execution time of the function called (in seconds)

    * also catches and logs any exceptions raised gracefully.
"""

import time
from functools import wraps

from logbook import Logger

__version__ = "1.0.4"


def iologger(function):
    """
    Decorator which logs the wrapped function/method.

    The following are logged:
        1. name of the function called
        2. arg(s) passed for the function called (if any)
        3. kwarg(s) passed for the function called (if any)
        4. execution time of the function called (in seconds)

        * also catches and logs any exceptions raised gracefully.

    :param function: func to run and all its args/kwargs.
    :return: returns func(*args, **kwargs)
    """

    logger = Logger("IOL - {}".format(function.__name__))

    @wraps(function)
    def wrapper(*args, **kwargs) -> None:
        with logger.catch_exceptions():
            logger.debug("Starting...")

            arg_dict = dict()
            arg_dict['args'] = args
            arg_dict['kwargs'] = kwargs
            logger.debug("passed args/kwargs = {}".format(arg_dict))

            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()

            logger.debug("returned: '{}'".format(result))
            logger.info("...Finished ({:1.2} seconds)".format(end - start))

            return result

    return wrapper
