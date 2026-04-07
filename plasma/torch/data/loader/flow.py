import torch

from typing import Callable
from ....parallel_processing import communicators, queues


class LoaderFlow(communicators.AsyncFlow):
    
    def __init__(
            self, ds:torch.utils.data.Dataset,
            workers:int,
            batch_size:int,
            num_prefetch:int,
            result_queue:queues.ThreadQueue,
            collator:Callable,
        ):
        super().__init__()
        
        self @ queues.ProcessQueue(workers) >> ds.__getitem__ \
            >> queues.ProcessQueue(qsize=batch_size) \
            >> Accumulator(batch_size, collator) \
            >> communicators.distributors.IteratorDistributor() \
            >> queues.TransferQueue(qsize=num_prefetch) \
            >> result_queue.put


class Accumulator:
    
    def __init__(self, batch_size:int, collator):
        self._data = []
        self.batch_size = batch_size
        self.collator = collator
    
    def __call__(self, d):
        data = self._data
        data.append(d)

        while len(data) >= self.batch_size:
            yield self.collator(data[:self.batch_size])
            data = data[self.batch_size:]
        
        self._data = data
        yield queues.Signal.IGNORE
