
from warnings import deprecated


@deprecated('this class will be removed in the future')
class FlowExceptionHandler:
    
    def run(self, block:str, data, e:Exception):
        raise e

    def __call__(self, block:str, data, e:Exception):
        return self.run(block, data, e)
