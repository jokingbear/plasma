import time
import multiprocessing as mp

from ....functional import State
from tqdm.auto import tqdm
from multiprocessing.managers import ValueProxy
from ...queues import Signal


class Accumulator[D, A](State):

    def __init__(self, total:int, sleep=1e-2, process_base=False, ignore_none=True, count_none=True):
        super().__init__()
        self._results = []

        process_queue = None if not process_base else mp.JoinableQueue()
        self._process_queue = process_queue
        self._counter:int|ValueProxy[int] = 0 if not process_base else mp.Value('i', 0)

        self._marked_attributes.append('finished')
        self.total = total
        self.sleep = sleep
        self.process_base = process_base
        self.ignore_none = ignore_none
        self.count_none = count_none
    
    def run(self, data):
        if data is not None or (data is None and self.count_none):
            self._update_step()

        if data is not None or (data is None and not self.ignore_none):
            self.aggregate(data)

        if self._process_queue is not None and self._counter.value == self.total:
            self._process_queue.put(self._results)
        
        if self.finished == self.total:
            return self.results
        
        return Signal.IGNORE

    def wait(self, **tqdm_kwargs):
        with tqdm(total=self.total, **tqdm_kwargs) as prog:
            n = self._counter
            prog.update(n)
            while not self.finished:
                time.sleep(self.sleep)
                new_n = self._counter
                diff = new_n - n
                n = new_n
                prog.update(diff)
        
        if self._process_queue is not None:
            self._results = self._process_queue.get()

        return self.results

    @property
    def results(self):
        return self.finalize()

    @property
    def finished(self) -> bool:
        value = self._counter
        if isinstance(self._counter, mp.Value):
            value = self._counter.value
        
        return value == self.total

    def release(self):
        self._results = []
        self._counter = 0 if not self.process_base else mp.Value('i', 0)

    def _update_step(self):
        if isinstance(self._counter, int):
            self._counter += 1
        else:
            self._counter.value += 1

    def aggregate(self, data:D):
        self._results.append(data)
    
    def finalize(self) -> A:
        return self._results
