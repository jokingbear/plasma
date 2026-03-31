from typing import Callable

from .chain import Chain
from .flow import Flow
from .operators import Init, Operator
from ..queues import Queue


class Resolver:
    
    def __init__(
            self, 
            data_qcreator:Callable[[], Queue], 
            join_qcreator:Callable[[], Queue]
        ):
        self.data_qcreator = data_qcreator
        self.join_qcreator = join_qcreator
    
    def __call__(self, chain:Chain):
        flow = Flow()
        ops = list[Operator]()
        while not isinstance(chain.op, Init):
            ops.append(chain.op)
            chain = chain.prevs
        ops = ops[::-1]

        return flow
