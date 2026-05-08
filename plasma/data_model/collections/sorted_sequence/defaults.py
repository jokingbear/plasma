from ...abc import Comparable


def identity[T:Comparable](x:T) -> T:
    return x


def abs_diff(x, y):
    return abs(x - y)
