from typing import Iterable
from .base import ParallelStream
from .pool import ThreadPool
from ...functional import pipe


def parallel[T](data:Iterable[T]):
    return ParallelStream(
        data, 
        ThreadPool(1, 0, pipe[T, T](lambda x:x))
    )
