import random
import sched

from typing import Callable, Sequence
from ...queues import Queue, Full
from ....functional import ReadableClass


class RoundRobinSharder(ReadableClass):
    
    def __init__(self, *queues:Queue):
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
    
    def schedule(self, 
            refresher:Callable[[],Sequence[Queue]],
            interval:float
        ):
        assert self._scheduler is None

        scheduler = sched.scheduler()
        def self_loop():
            self.queues = refresher()
            scheduler.enter(interval, 0, self_loop)
        
        self._scheduler = scheduler # ref so gc wont collect
        self_loop()
