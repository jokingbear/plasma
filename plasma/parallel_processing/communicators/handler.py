
from warnings import deprecated, warn
from ...utils import Formatter


@deprecated('this class will be removed in the future')
class FlowExceptionHandler:
    
    def __init__(self):
        warn(
            Formatter.YELLOW('this class will be remove in the next version'),
            stacklevel=2
        )
    
    def run(self, block:str, data, e:Exception):
        raise e

    def __call__(self, block:str, data, e:Exception):
        return self.run(block, data, e)
