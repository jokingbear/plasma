from typing import Hashable
from pathlib import Path


class Meta:
    
    def __init__(self):
        self._contexts:dict[Path, set] = {}
    
    def init(self, context):
        if context not in self:
            self._contexts[context] = set()
    
    def add_name(self, context:Path, name:str):
        self._contexts[context].add(name)
    
    def __iter__(self):
        for c in self._contexts:
            yield c
    
    def __getitem__(self, context:Path):
        return self._contexts[context]
    
    def __contains__(self, other:Path):
        return other in self._contexts
    
    def __repr__(self):
        lines = []
        lines.extend(f'{context}: {', '.join(names)}' 
                     for context, names in self._contexts.items())
        return '\n'.join(lines)
