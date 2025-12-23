from .decorator import Timer


def timer(func):
    return Timer()(func)
