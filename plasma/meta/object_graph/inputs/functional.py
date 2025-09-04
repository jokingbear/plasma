import re

from .file_reader import ReadInputs
from ..managed import AutoContext
from enum import Enum


class InitiableInputs(ReadInputs):
    
    def init(self, context:AutoContext, *names:str, verbose=True):
        requirements = context.inputs(*names)
        
        if verbose:
            context_rep = repr(context)
            for n in names:
                context_rep = re.sub(rf'\W({n})\W', Color.GREEN.render, context_rep)
            
            for k, req in requirements.items():
                color = Color.RED
                if k in context.context_manager:
                    color = Color.CYAN

                context_rep = re.sub(rf'\W({k})\W', color.render, context_rep)
            
            print(context_rep)
        
        inputs = self.to_dict()
        return context.run(*names, **inputs)
        

class Color(Enum):
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
   def render(self, match:re.Match):
        return f'{self.value}{match.group(0)}{self.END.value}'
