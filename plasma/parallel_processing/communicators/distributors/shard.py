import threading

from ...queues import Queue, Full
from ....functional import ReadableClass


class RoundRobinSharder(ReadableClass):
    
    def __init__(self, *queues:Queue):
        self.queues = queues
        self._lock = threading.Lock()
        self._counter = 0
    
    def __call__(self, data):
        with self._lock:
            counter = self._counter
            while True:
                try:
                    self.queues[counter].put(data)
                    break
                except Full:
                    print('load balancing')
                finally:
                    self._counter = (counter + 1) % len(self.queues)
