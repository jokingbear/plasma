import json
import re

from .file_reader import ReadInputs


class RenderableInputs(ReadInputs):
    
    def to_dict(self):
        results = {}
        for k in self.__annotations__:
            if hasattr(self, k):
                value = getattr(self, k)
                if isinstance(value, ReadInputs):
                    value = value.to_dict()
                
                results[k] = value

        return results
    
    def __repr__(self):
        rep = json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
        rep = re.sub(r'"(.+?)"\:', r'\1:', rep)
        return rep
