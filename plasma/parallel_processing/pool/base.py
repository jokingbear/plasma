from typing import Iterable
from uuid import uuid4

from .chain import Chain
from .operators import Init
from .stream import Stream
from .resolver import Resolver
from ..queues import Queue
from ...functional import ReadableClass


class Pool(ReadableClass):
    
    def __init__(self, num_workers:int):
        super().__init__()
        
        self.resolver = Resolver(num_workers, self._create_data_queue, self._create_join_queue)
    
    def stream[T](self, data:Iterable[T]):
        id = uuid4()
        return Stream(id, data, Chain(None, Init[T]()), self.resolver)
    
    def _create_data_queue(self, num_worker:int) -> Queue:...
    
    def _create_join_queue(self) -> Queue:...
    