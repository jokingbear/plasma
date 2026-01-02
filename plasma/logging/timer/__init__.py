from .timeio import TimeIO
from .decorator import Timer


def time(func):
    return Timer()(func)
