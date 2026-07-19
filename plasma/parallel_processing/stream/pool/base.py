from dataclasses import dataclass
from typing import Callable, Any
from ...communicators import AsyncFlow
from ...queues import Queue
from ....functional import pipe


@dataclass(frozen=True)
class Pool[I, O]:
    num_worker:int
    qsize:int
    func: pipe[I, O]
    prev: "Pool[Any, I] | None" = None 
    
    def init_queue(self) -> Queue: ...

    def compile(self):
        qf_pairs = list[tuple[Queue, Callable]]()
        current = self
        while current is not None:
            qf_pairs.append((current.init_queue(), current.func))
            current = current.prev
        
        qf_pairs = qf_pairs[::-1]
        flow = AsyncFlow()
        
        q0, f0 = qf_pairs[0]
        chain = flow @ q0 >> f0
        for q, f in qf_pairs[1:]:
            chain = chain >> q >> f
        return flow
