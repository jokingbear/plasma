from .base import Pool
from ..queues import ThreadQueue, ProcessQueue, TransferQueue


class Thread(Pool):
    
    def __init__(self, num_workers, prefetch=0):
        super().__init__(num_workers)
        
        self.prefetch = prefetch
    
    def _create_data_queue(self, num_worker):
        return ThreadQueue(num_worker, qsize=self.prefetch)
    
    def _create_join_queue(self):
        return ThreadQueue(1, qsize=self.prefetch)


class Process(Pool):

    def __init__(self, num_workers, prefetch=0):
        super().__init__(num_workers)
        
        self.prefetch = prefetch

    def _create_data_queue(self, num_worker):
        return ProcessQueue(num_worker, qsize=self.prefetch)

    def _create_join_queue(self):
        return TransferQueue(qsize=self.prefetch)
