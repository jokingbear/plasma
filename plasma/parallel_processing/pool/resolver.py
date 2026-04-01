from typing import Callable

from .chain import Chain
from .flow import Flow
from .operators import Init, Operator
from .utils import StreamAccumulator
from ..queues import Queue
from ..communicators import Accumulator
from ..communicators.distributors import Distributor
from ...functional import chain


class Resolver:
    
    def __init__(
            self, num_worker:int,
            data_qcreator:Callable[[int], Queue], 
            join_qcreator:Callable[[], Queue]
        ):
        self.num_workers = num_worker
        self.data_qcreator = data_qcreator
        self.join_qcreator = join_qcreator
    
    def __call__(self, chain:Chain):
        flow = Flow()
        ops = self.build_ops(chain)
        merged_ops = self.merge_ops(ops)
        
        num_bucket = len([
            op for op in merged_ops
            if isinstance(op, tuple) or not (isinstance)
        ]) 
        for op in merged_ops:
            pass
        
        return flow

    def build_ops(self, chain:Chain):
        ops = list[Operator]()
        while not isinstance(chain.op, Init):
            ops.append(chain.op)
            chain = chain.prevs
        ops = ops[::-1]
        if not isinstance(ops[-1], Accumulator):
            ops.append(StreamAccumulator())

        return ops

    def merge_ops(self, ops:tuple[Operator,...]):
        merged = []
        for op in ops:
            if len(merged) == 0:
                merged.append(op)
            elif isinstance(op, Distributor):
                merged[-1] = (merged[-1], op)
            elif len(merged) > 0 and not isinstance(merged[-1], (tuple, Accumulator)):
                merged[-1] = chain(merged[-1], op)
            else:
                merged.append(op)
        
        return merged

    def create_queue(self, ops):
        pass
