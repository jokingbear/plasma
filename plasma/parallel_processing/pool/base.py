from ..communicators import AsyncFlow
from ..queues import Queue
from ...functional import AutoPipe, auto_map_func
from ..communicators.accumulators import DynamicAccumulator
from typing import Callable


class Pool:
    
    def __init__(self, 
                iq:Queue, oq:Queue, 
                **global_vars
        ):        
        runner = FuncRunner(global_vars)
        runner = auto_map_func(runner)
        accumalator = Accumulator()
        
        flow = AsyncFlow().chain(
            (iq, runner),
            (runner, oq, accumalator)
        )
        self._flow = flow
        self._accumulator = accumalator
    
    def __enter__(self):
        self._flow.__enter__()
        return self

    def __exit__(self, *_):
        self._flow.__exit__(*_)
    
    def map(self, array:list, func:Callable, **tqdm_kwargs) -> list:
        try:
            for i, item in enumerate(array):
                self._flow.put((i, func, item))

            return self._accumulator.wait(len(array), **tqdm_kwargs)
        finally:
            self._accumulator.release()


class FuncRunner(AutoPipe):
    
    def __init__(self, vars):
        super().__init__()
        self.vars = vars
    
    def run(self, task_id, func, input):
        return task_id, func(input, **self.vars)


class Accumulator(DynamicAccumulator[object, list]):
    
    def finalize(self):
        results = sorted(self._results, key=lambda r:r[0])
        results = [r for _, r in results]
        return results
