from ...functional import AutoPipe, chain
from typing import Callable


class InitPipe[T](AutoPipe):
    
    def run(self, rank:int) -> T:
        pass
    
    def chain(self, function):
        return ChainPipe(self, function)


class ChainPipe(InitPipe[Callable]):
    
    def __init__(self, init_pipe:InitPipe, new_func):
        super().__init__()
        
        self.original_pipe = init_pipe
        self.chainer = new_func
    
    def run(self, rank):
        processor1 = self.original_pipe.run(rank)
        processor2 = self.chainer
        if isinstance(processor2, InitPipe): 
            processor2 = processor2.run(rank)
        
        return chain(processor1, processor2)
