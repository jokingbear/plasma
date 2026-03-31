from typing import Iterable
from uuid import uuid4

from .chain import Chain
from .operators import Init
from .stream import Stream
from .resolver import Resolver

from ..queues import Queue


class Pool:
    
    def __init__(self, num_workers:int):
        self.resolver = Resolver()
    
    def stream[T](self, data:Iterable[T]):
        id = uuid4()
        return Stream(id, data, Chain(None, Init[T]()), self.resolver)
    
    def _create_data_queue(self) -> Queue:...
    
    def _create_join_queue(self) -> Queue:...
    