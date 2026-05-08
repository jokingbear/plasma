from ..communicators.accumulators import DynamicAccumulator
from ...functional.decorators import propagate


class Invalid:...

class End:...


class StreamAccumulator(DynamicAccumulator):
    
    def __init__(self):
        super().__init__(ignore_none=False)
        
    @propagate(Invalid)
    def aggregate(self, data):
        return super().aggregate(data)
