from typing import Callable

from plasma.parallel_processing.queues import (
    Queue, ThreadQueue, TransferQueue, ProcessQueue
)
from .base import Pool
from ....functional import pipe


class ThreadPool[I, O](Pool[I, O]):
    
    def map[T](self, func:Callable[[O], T]):
        new_func = self.func.chain(func)
        return ThreadPool(
            self.num_worker, self.qsize,
            new_func, self.prev
        )

    def thread_map[T](self, func:Callable[[O], T], num_worker:int, qsize:int=0):
        return ThreadPool(
            num_worker, qsize, pipe(func), self
        )

    def process_map[T](self, func:Callable[[O], T], num_worker:int, qsize:int=0):
        return ProcessPool(
            num_worker, qsize, pipe(func), self
        )

    def init_queue(self):
        if isinstance(self.prev, ProcessPool):
            q = TransferQueue(n=self.num_worker, qsize=self.qsize)
        else:
            q = ThreadQueue(n=self.num_worker, qsize=self.qsize)
        return q
    

class ProcessPool[I, O](Pool[I, O]):

    def map[T](self, func:Callable[[O], T]):
        new_func = self.func.chain(func)
        return ProcessPool(
            self.num_worker, self.qsize, new_func, self.prev
        )

    def thread_map[T](self, func:Callable[[O], T], num_worker:int, qsize:int=0):
        return ThreadPool(
            num_worker, qsize, pipe(func), self
        )
    
    def process_map[T](self, func:Callable[[O], T], num_worker:int, qsize:int=0):
        return ProcessPool(
            num_worker, qsize, pipe(func), self
        )

    def init_queue(self):
        return ProcessQueue(self.num_worker, qsize=self.qsize)
