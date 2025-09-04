import json
import re

from .functional import InitiableInputs as Inputs
from ....functional import AutoPipe


class RenderableInputs(Inputs):
    
    def to_dict(self):
        results = {}
        for k in self.__annotations__:
            if hasattr(self, k):
                value = getattr(self, k)
                if isinstance(value, Inputs):
                    value = value.to_dict()
                
                results[k] = value

        return results
    
    def __repr__(self):
        rep = json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=default)
        rep = re.sub(r'"(.+?)"\:', r'\1:', rep)
        return rep


def default(obj):
    return type(obj).__name__
