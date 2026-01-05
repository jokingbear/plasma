import re

from .file_reader import ReadInputs
from enum import Enum
from .....functional.helpers.color_printer import Color
from ..context import Context


class InitiableInputs(ReadInputs):
    
    def init(self, context:Context, *names:str, verbose=True):
        if verbose:
            context_rep = repr(context)
            for n in names:
                context_rep = re.sub(rf'\W({n})\W', lambda m: Color.GREEN(m.group(0)), context_rep)
            
            print(context_rep)
        
        inputs = self.to_dict()
        return context.run(*names, **inputs)
