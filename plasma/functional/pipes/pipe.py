from abc import abstractmethod
from .readable import ReadableClass


class AutoPipe(ReadableClass):

    @abstractmethod
    def run(self, *inputs, **kwargs):
        pass
    
    def __init_subclass__(cls):
        cls.__call__ = cls.run
