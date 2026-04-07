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


class ItemGetter:
    
    def __init__(self, dataset):
        self.dataset = dataset
    
    def __call__(self, arg):
        try:
            return self.dataset[arg]
        except Exception as e:
            return e


class Accumulator:
    
    def __init__(self, batch_size:int, collator):
        self._data = []
        self.batch_size = batch_size
        self.collator = collator
    
    def __call__(self, d):
        if isinstance(d, Exception):
            yield d
        else:
            data = self._data
            data.append(d)

            while len(data) >= self.batch_size:
                try:
                    yield self.collator(data[:self.batch_size])
                    data = data[self.batch_size:]
                except Exception as e:
                    yield e
                    data = []
                    break
                
            self._data = data
            yield queues.Signal.IGNORE
