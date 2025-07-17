from ...functional import AutoPipe


class TorchPipe(AutoPipe):
    
    def process_init(self, rank:int)->None:
        pass
    
    def chain(self, function):
        return ChainPipe(self, function)


class ChainPipe(TorchPipe):
    
    def __init__(self, torch_pipe:TorchPipe, new_func):
        super().__init__()
        
        self.original_pipe = torch_pipe
        self.chainer = new_func
    
    def process_init(self, rank):
        self.original_pipe.process_init(rank)
        
        if isinstance(self.chainer, TorchPipe):
            self.chainer.process_init(rank)
    
    def run(self, *inputs, **kwargs):
        results = self.original_pipe.run(*inputs, **kwargs)
        return self.chainer(results)
