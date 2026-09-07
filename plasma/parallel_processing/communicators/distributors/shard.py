import random

from collections.abc import Sequence
from ...queues import Queue, Full
from ....functional import ReadableClass


class RoundRobinSharder(ReadableClass):
    
    def __init__(self, *queues:Queue):
        super().__init__()

        self.queues = queues
        self._scheduler = None
    
    def __call__(self, data):
        queues = self.queues
        rng = random.Random()
        counter = rng.choice(range(len(queues)))
        while True:
            try:
                queues[counter].put(data)
                break
            except Full:
                print('load balancing')
            finally:
                counter = (counter + 1) % len(queues)
    
    def refresh(self, new_queues:Sequence[Queue]):
        self.queues = new_queues
