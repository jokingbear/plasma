import random

from ...queues import Queue, Full
from ....functional import ReadableClass


class RoundRobinSharder(ReadableClass):
    
    def __init__(self, *queues:Queue):
        self.queues = queues
    
    def __call__(self, data):
        rng = random.Random()
        counter = rng.choice(range(len(self.queues)))
        while True:
            try:
                self.queues[counter].put(data)
                break
            except Full:
                print('load balancing')
            finally:
                counter = (counter + 1) % len(self.queues)
