from .pipe import AutoPipe
from abc import abstractmethod


class SimplePipe[I, O](AutoPipe):

    @abstractmethod
    def run(self, inputs:I)->O:
        pass

    def __call__(self, inputs:I) -> O:
        return self.run(inputs)



class I2O[I1, I2, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2) -> O:
        pass
    
    def __call__(self, input1:I1, input2:I2):
        return self.run(input1, input2)
    

class I3O[I1, I2, I3, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2, input3: I3) -> O:
        pass
    
    def __call__(self, input1:I1, input2:I2, input3: I3):
        return self.run(input1, input2, input3)
    

class I4O[I1, I2, I3, I4, O](AutoPipe):
    
    @abstractmethod
    def run(self, input1:I1, input2:I2, input3: I3, input4:I4) -> O:
        pass
    
    def __call__(self, input1:I1, input2:I2, input3: I3, input4:I4):
        return self.run(input1, input2, input3, input4)
