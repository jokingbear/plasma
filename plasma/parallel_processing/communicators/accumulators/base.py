import time

from tqdm.auto import tqdm
from ....functional import ReadableClass
from ...queues import Signal


class Accumulator[D, A](ReadableClass):

    def __init__(self, total:int, sleep=1e-2, ignore_none=True, count_none=True):
        super().__init__()
        
        self._results = []
        self._counter = 0

        self._marked_attributes.append('finished')
        self.total = total
        self.sleep = sleep
        self.ignore_none = ignore_none
        self.count_none = count_none
    
    def __call__(self, data):
        if data is not None or (data is None and self.count_none):
            self._update_step()

        if data is not None or (data is None and not self.ignore_none):
            self.aggregate(data)
        
        if self.finished == self.total:
            return self.results
        
        return Signal.IGNORE

    def wait(self, **tqdm_kwargs):
        with tqdm(total=self.total, **tqdm_kwargs) as prog:
            n = self._counter
            prog.update(n) #type:ignore
            while not self.finished:
                time.sleep(self.sleep)
                new_n = self._counter
                diff = new_n - n #type:ignore
                n = new_n
                prog.update(diff)

        return self.results

    @property
    def results(self):
        return self.finalize()

    @property
    def finished(self) -> bool:
        value = self._counter
        return value == self.total

    def release(self):
        self._results = []
        self._counter = 0

    def _update_step(self):
        if isinstance(self._counter, int):
            self._counter += 1
        else:
            self._counter.value += 1

    def aggregate(self, data:D):
        self._results.append(data)
    
    def finalize(self) -> A:
        return self._results #type:ignore
