import re

from .file_reader import ReadInputs
from ..managed import AutoContext
from enum import Enum
from ....functional.helpers.color_printer import Color


class InitiableInputs(ReadInputs):
    
    def init(self, context:AutoContext, *names:str, verbose=True):
        if verbose:
            requirements = context.inputs(*names, include_singleton=True)
            context_rep = repr(context)
            for n in names:
                context_rep = re.sub(rf'\W({n})\W', lambda m: Color.GREEN(m.group(0)), context_rep)
            
            for k, req in requirements.items():
                color = Color.RED
                if k in context.context_manager:
                    color = Color.CYAN
                elif req is not context.requirement:
                    color = Color.YELLOW

                context_rep = re.sub(rf'\W({k})\W', lambda m: color(m.group(0)), context_rep)
            
            print(context_rep)
        
        inputs = self.to_dict()
        return context.run(*names, **inputs)
