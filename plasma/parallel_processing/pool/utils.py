from ..communicators.accumulators import DynamicAccumulator
from ...functional.decorators import propagate


class Invalid:...

class End:...


class StreamAccumulator(DynamicAccumulator):
    
    def __init__(self):
        super().__init__()
        
        self._end = False 
    
    def run(self, data):
        self._end = data is End
        return super().run(data)
    
    @propagate(End)
    @propagate(Invalid)
    def aggregate(self, data):
        return super().aggregate(data)

    @property
    def finished(self):
        return self._end
