from ..communicators.accumulators import DynamicAccumulator
from ...functional.decorators import propagate


class Invalid:...

class End:...


class StreamAccumulator(DynamicAccumulator):
    
    def __init__(self):
        super().__init__(0, ignore_none=False)
        
        self._end = False 
        
    @propagate(Invalid)
    def aggregate(self, data):
        return super().aggregate(data)

    @property
    def finished(self):
        return self._end
