from .base import Pool
from ..queues import ThreadQueue, ProcessQueue, TransferQueue


class ThreadPool(Pool):
    
    def _create_data_queue(self, num_worker):
        return ThreadQueue(num_worker)
    
    def _create_join_queue(self):
        return ThreadQueue(1)


class ProcessPool(Pool):
    
    def _create_data_queue(self, num_worker):
        return ProcessQueue(num_worker)

    def _create_join_queue(self):
        return TransferQueue()
