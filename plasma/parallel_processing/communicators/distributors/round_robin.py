from .base import Distributor
from queue import Full


class RoundRobin(Distributor):
    
    def __init__(self, num_workers:int):
        super().__init__()
        
        self.num_workers = num_workers
        self._counters = 0
    
    def run(self, data, *queues, **named_queues):
        is_pushing = True
        while is_pushing:
            try:
                queues[self._counters].put(data)
            except Full:
                print('load balancing')
            finally:
                self._counters = (self._counters + 1) % self.num_workers
        