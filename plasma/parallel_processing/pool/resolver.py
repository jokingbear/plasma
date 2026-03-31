from typing import Callable

from .chain import Chain
from .flow import Flow
from .operators import Init, Operator
from .utils import StreamAccumulator
from ..queues import Queue
from ..communicators import Accumulator


class Resolver:
    
    def __init__(
            self, 
            data_qcreator:Callable[[int], Queue], 
            join_qcreator:Callable[[], Queue]
        ):
        self.data_qcreator = data_qcreator
        self.join_qcreator = join_qcreator
    
    def __call__(self, chain:Chain):
        flow = Flow()
        ops = self.build_ops(chain)

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
