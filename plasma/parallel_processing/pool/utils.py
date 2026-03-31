from typing import Callable


def chain[T, U, V](
        f1:Callable[[T], U],
        f2:Callable[[U], V]
    ):
    
    def chained(inputs:T):
        return f2(f1(inputs))
    
    return chained


class Invalid:...
