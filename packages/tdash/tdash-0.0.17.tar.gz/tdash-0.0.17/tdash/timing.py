from functools import wraps
from time import time


def measure_time(name=None):
    def decorator(func):
        called = name if name else func.__name__

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            t0 = time()
            result = func(*args, **kwargs)
            t = time() - t0
            print(called, t)
            return result
        return func_wrapper
    return decorator


class Stopwatch(object):
    def __init__(self, inside_mg='Default watch,'):
        self.start_time = time()
        self.inside_mg = inside_mg

    def print_time(self, msg):
        print(self.inside_mg, 'Time: ', msg, ':   ', time() - self.start_time)
        self.start_time = time()
