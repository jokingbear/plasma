from typing import Sequence
from .base import Distributor


class IteratorDistributor[T](Distributor[Sequence[T]]):
    
    def run(self, data, *queues, **named_queues):  
        for r in data:
            for q in queues:
                q.put(r)

            for q in named_queues.values():
                q.put(r)
