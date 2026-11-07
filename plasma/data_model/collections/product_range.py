import itertools


def product_range(*ranges:int):
    return itertools.product(*[range(r) for r in ranges])
