from collections.abc import Sequence
from collections import deque
from typing import final


@final
class Accessor:
    
    def __init__(self,
            name:str, parent:'Accessor|None'=None,
            children:Sequence['Accessor']=(),
        ):
        assert ' ' not in name, 'accessor name cannot contain space'

        self._name = name
        self._parent = parent
        
        for c in children:
            c._parent = self
        self._children = {a._name: a for a in children if a._name is not None}
    
    def __repr__(self):
        names = deque()
        accessor = self
        while True:
            names.appendleft(accessor._name)
            
            if accessor._parent is None:
                break

            accessor = accessor._parent
        return '.'.join(names)
    
    def __getattr__(self, name):
        children = object.__getattribute__(self, '_children')
        if name in children:
            return children[name]
        else:
            return object.__getattribute__(self, name)
        
    def __eq__(self, value: object):
        return (
            isinstance(value, Accessor)
            and self._name == value._name
            and self._parent == value._parent
        )

    def __hash__(self):
        name = repr(self)
        return hash(name)

    @staticmethod
    def get_name(a:'Accessor'):
        return a._name
    
    @staticmethod
    def get_parent(a:'Accessor'):
        return a._parent

    @staticmethod
    def get_children(a:'Accessor'):
        yield from a._children.values()
