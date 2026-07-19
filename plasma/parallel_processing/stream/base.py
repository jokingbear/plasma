from typing import Iterable, Callable, Any
from .pool import ThreadPool, ProcessPool
from ..communicators import DynamicAccumulator
from ...data_model.collections import Stream


class ParallelStream[I]:
    
    def __init__(self, 
            data:Iterable,
            pool:ThreadPool[Any, I]|ProcessPool[Any, I]
        ):
        self.__data = data
        self.__pool = pool
    
    def select[O](self, func:Callable[[I], O]):
        return ParallelStream(self.__data, self.__pool.map(func))

    def thread_select[O](self, 
            func:Callable[[I], O], *,
            num_worker:int, qsize:int=100
        ):
        return ParallelStream(
            self.__data,
            self.__pool.thread_map(func, num_worker, qsize)
        )

    def process_select[O](self,             
            func:Callable[[I], O], *,
            num_worker:int, qsize:int=100
        ):
        return ParallelStream(
            self.__data,
            self.__pool.process_map(func, num_worker, qsize)
        )

    def evaluate(self, **tqdm_kwargs):
        accumulator = DynamicAccumulator[Any, list[I]](ignore_none=False)
        
        flow = (
            self.__pool.thread_map(accumulator, 1)
            .compile()
        )
        counter = 0
        print(flow)
        with flow:
            for d in self.__data:
                flow.put(d)
                counter += 1
            
            return Stream(accumulator.wait(counter, **tqdm_kwargs))
