from .base import Pool
from ..queues import ThreadQueue, ProcessQueue, TransferQueue


class ThreadPool(Pool):
    
    def __init__(self, num_workers, prefetch=0):
        super().__init__(num_workers)
        
        self.prefect = prefetch
    
    def _create_data_queue(self, num_worker):
        return ThreadQueue(num_worker, qsize=self.prefect)
    
    def _create_join_queue(self):
        return ThreadQueue(1, qsize=self.prefect)


class ProcessPool(Pool):

    def __init__(self, num_workers, prefetch=0):
        super().__init__(num_workers)
        
        self.prefect = prefetch

    def _create_data_queue(self, num_worker):
        return ProcessQueue(num_worker)

    def _create_join_queue(self):
        return TransferQueue()
