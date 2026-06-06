import re

from .file_reader import ReadInputs
from ..context import Context
from .....utils import Formatter


class InitiableInputs(ReadInputs):
    
    def init(self, context:Context, *names:str, verbose=True):
        if verbose:
            context_rep = repr(context)
            for n in names:
                context_rep = re.sub(rf'\W({n})\W', lambda m: Formatter.GREEN(m.group(0)), context_rep)
            
            print(context_rep)
        
        inputs = self.to_dict()
        return context.run(*names, **inputs)
