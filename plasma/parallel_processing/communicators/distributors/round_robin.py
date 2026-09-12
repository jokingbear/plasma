import random

from queue import Full
from .base import Distributor



class RoundRobin[T](Distributor[T]):
    
    def __init__(self, num_workers:int, verbose=True):
        super().__init__()
        
        self.num_workers = num_workers
        self.verbose = verbose
    
    def run(self, data, *queues, **named_queues):
        rng = random.Random()
        counter = rng.choice(range(self.num_workers))
        while True:
            try:
                queues[counter].put(data)
                break
            except Full:
                print('load balancing') if self.verbose else None
            finally:
                counter = (counter + 1) % self.num_workers
