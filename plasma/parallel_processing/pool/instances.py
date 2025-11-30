from .base import Pool
from ..queues import ThreadQueue, ProcessQueue, TransferQueue


class ThreadPool(Pool):
    
    def __init__(self, workers:int, **global_vars):
        iq = ThreadQueue(workers)
        oq = ThreadQueue()
        super().__init__(iq, oq, **global_vars)


class ProcessPool(Pool):
    
    def __init__(self, workers:int, **global_vars):
        iq = ProcessQueue(workers)
        oq = TransferQueue()
        super().__init__(iq, oq, **global_vars)
