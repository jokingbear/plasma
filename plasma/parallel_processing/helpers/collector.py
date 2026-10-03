import gc

from ...functional import ReadableClass


class GarbageCollector(ReadableClass):
    
    def __init__(self, *, threshold:int=1000):
        super().__init__()
        
        self.threshold = threshold
        self._counter = 0
        
    def __call__(self, _):
        self._counter += 1
        
        if self._counter % self.threshold == 0:
            gc.collect()
            self._counter = 0
