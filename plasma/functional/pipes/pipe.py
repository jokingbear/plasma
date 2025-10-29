from abc import abstractmethod
from .readable import ReadableClass


class AutoPipe(ReadableClass):

    @abstractmethod
    def run(self, *inputs, **kwargs):
        pass
    
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)
