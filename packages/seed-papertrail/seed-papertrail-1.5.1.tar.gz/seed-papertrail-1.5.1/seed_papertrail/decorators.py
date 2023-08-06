from functools import wraps
from contextlib import contextmanager
import logging
import time
import sys
import random


# NOTE: got this from http://stackoverflow.com/a/14412901
def doublewrap(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    '''
    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


class PapertrailHelper(object):

    DEFAULT_THRESHOLDS = {
        'OK': (0.0, 0.6),
        'WARNING': (0.6, 1.0),
        'CRITICAL': (1.0, sys.maxsize),
    }

    def __init__(self):
        self.debug = self.make_decorator('DEBUG', logger='papertrail')
        self.info = self.make_decorator('INFO', logger='papertrail')
        self.error = self.make_decorator('ERROR', logger='papertrail')
        self.warn = self.make_decorator('WARNING', logger='papertrail')

    def __call__(self, message, level='DEBUG', logger='papertrail'):
        return self.make_decorator(level, logger)(message)

    def threshold_display(self, duration, thresholds):
        [threshold] = filter(
            lambda kv: kv[1][0] <= duration < kv[1][1],
            thresholds.items())
        return threshold[0]

    def make_decorator(self, level, logger):
        logger = logging.getLogger(logger)

        @doublewrap
        def decorator(f, message='', sample=1.0,
                      thresholds=self.DEFAULT_THRESHOLDS):
            @wraps(f)
            def wrap(*args, **kwargs):
                start = time.clock()
                resp = f(*args, **kwargs)
                duration = time.clock() - start
                if random.random() <= sample:
                    logger.log(
                        getattr(logging, level),
                        '%s.%s %f: %s, threshold:%s, sampling:%s' % (
                            f.__module__,
                            f.__name__,
                            duration,
                            message,
                            self.threshold_display(duration, thresholds),
                            sample,
                        ))
                return resp
            return wrap
        return decorator

    @contextmanager
    def timer(self, message, level='DEBUG', logger='papertrail',
              thresholds=DEFAULT_THRESHOLDS):
        logger = logging.getLogger(logger)
        start = time.time()
        yield logger
        duration = time.time() - start
        [threshold] = filter(
            lambda kv: kv[1][0] <= duration < kv[1][1],
            thresholds.items())
        logger.log(
            getattr(logging, level),
            '%f: %s, threshold:%s' % (
                duration, message,
                self.threshold_display(duration, thresholds)))


papertrail = PapertrailHelper()
