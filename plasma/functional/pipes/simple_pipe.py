from .pipe import AutoPipe
from abc import abstractmethod


class SimplePipe[I, O](AutoPipe):

    @abstractmethod
    def run(self, inputs:I, **kwargs)->O:
        pass


class I2O[I1, I2, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2, **kwargs) -> O:
        pass
    

class I3O[I1, I2, I3, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2, input3: I3, **kwargs) -> O:
        pass
    

class I4O[I1, I2, I3, I4, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2, input3: I3, input4:I4, **kwargs) -> O:
        pass
