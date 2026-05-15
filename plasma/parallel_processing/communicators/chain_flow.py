from typing import Callable, overload

from .async_flow import AsyncFlow
from .distributors import Distributor
from ..queues import Queue


class ChainFlow(AsyncFlow):
    
    def __init__(self):
        super().__init__()

    def __matmul__(self, other:Queue|Callable):
        if isinstance(other, Queue):
            return QueueChainer(self, other)

        return BlockChainer(self, other)


class QueueChainer:
    
    def __init__(self, flow:AsyncFlow, q:Queue):
        self.q = q
        self.flow = flow

    def __rshift__(self, other:Callable|Distributor):
        assert not isinstance(other, Queue), 'cannot chain consecutive Queue'
        self.flow.chain((self.q, other))
        return BlockChainer(self.flow, other)


class BlockChainer:
    
    def __init__(self, flow:AsyncFlow, block:Callable|Distributor):
        self.flow = flow
        self.block = block
    
    @overload
    def __rshift__(self, other:Queue) -> QueueChainer:...

    @overload
    def __rshift__(self, other:Callable|Distributor) -> "BlockChainer":...
    
    def __rshift__(self, other:Callable|Distributor|Queue):
        if isinstance(other, Queue):
            self.flow.chain((self.block, other))
            return QueueChainer(self.flow, other)
        
        elif id(other) in self.flow.graph:
            self.flow.chain((self.block, other))
            return BlockChainer(self.flow, other)
        
        elif isinstance(other, Distributor):
            assert not isinstance(self.block, Distributor), 'cannot chain consecutive distributor'
            qid, = self.flow.graph.predecessors(id(self.block))
            q = self.flow.graph.nodes[qid]['object']
            self.flow.chain((q, self.block, other))
            return self
        
        else:
            self.flow.chain((self.block, other))
            return BlockChainer(self.flow, other)
