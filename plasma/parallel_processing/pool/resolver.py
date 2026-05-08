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
        ops = self.build_ops(chain)
        merged_ops = self.merge_ops(ops)
        
        num_bucket = len([
            op for op in merged_ops
            if not isinstance(op, (Distributor, Accumulator))
        ])      
        return self.create_flow(merged_ops, self.num_workers // num_bucket)

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
            if len(merged) == 0 or isinstance(op, (Distributor, Accumulator)):
                merged.append(op)
            elif not isinstance(merged[-1], (Distributor, Accumulator)):
                merged[-1] = chain(merged[-1], op)
            else:
                merged.append(op)
        
        return merged

    def create_flow(self, ops, num_workers):
        flow = Flow()
        prev_op = None
        for op in ops:
            if isinstance(op, (Distributor, Accumulator)):
                pipe = self.join_qcreator(), op
            else:
                pipe = self.data_qcreator(num_workers), op
            
            if prev_op is None:
                flow.chain(pipe)
            else:
                flow.chain((prev_op, *pipe))
            prev_op = op

        flow.accumulator = prev_op
        return flow
