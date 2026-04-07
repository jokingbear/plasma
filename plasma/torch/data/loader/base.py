from queue import Queue
from torch.utils.data import Dataset
from typing import Callable

from .flow import LoaderFlow
from ....functional import ReadableClass, Identity


class ProcessLoader(ReadableClass):
    
    def __init__(
            self, dataset:Dataset,
            workers:int = 8,
            batch_size:int = 32,
            num_prefetch:int = 2,
            collator:Callable = None,
        ):
        super().__init__()
        
        self.dataset = dataset
        self.workers = workers
        self.batch_size = batch_size
        self.num_prefetch = num_prefetch
        self.collator = collator
        
        self._queue = Queue(maxsize=batch_size * num_prefetch)
        self.__len = len(dataset) // batch_size
    
    def __len__(self):
        return self.__len

    def __iter__(self):
        flow =LoaderFlow(
                self.dataset, 
                self.workers, self.batch_size, 
                self.num_prefetch, self._queue,
                self.collator or Identity()
            ) 
        with flow:
            for i in range(len(self.dataset)):
                flow.put(i)
            
            for i in range(len(self)):
                yield self._queue.get()
