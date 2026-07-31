from collections.abc import Generator, Sequence
from typing import get_origin, get_args
from types import UnionType

from .arch import SCHEMA
from ..accessor import Accessor
from ....functional import ReadableClass


class Schema[T](ReadableClass):
    
    def __init__(self, root:type[T]):
        super().__init__()
        self.root = root
        
        for attr, anno in root.__annotations__.items():
            anno_val = anno
            origin = get_origin(anno)
            if hasattr(anno, SCHEMA):
                anno_val = getattr(anno, SCHEMA)
            elif origin is not None and issubclass(origin, Sequence):
                generic_arg, = get_args(anno)
                if hasattr(anno, SCHEMA):
                    anno_val = AtItem(origin, getattr(generic_arg, SCHEMA))

            setattr(self, attr, anno_val)
    
    @property
    def accessors(self) -> Generator[Accessor]:
        for attr in self.root.__annotations__:
            val = getattr(self, attr)
            
            if isinstance(val, Schema|AtItem):
                for a in val.accessors:
                    yield a.prepend(attr)
            else:
                yield Accessor(attr)
    
    def _root_repr(self):
        return self.root.__name__
    
    def _tree(self, tree):
        for a in self.root.__annotations__:
            val = getattr(self, a)
            if isinstance(val, Schema):
                child = tree.add(f'{a}: {val.root.__name__}')
                val._tree(child)
            elif isinstance(val, AtItem):
                child = tree.add(f'{a}: {val.original.__name__}[{val.schema.root.__name__}]')
                child = child.add(val._root_repr())
                val._tree(child)
            elif isinstance(val, UnionType):
                tree.add(f'{a}: {val}')
            else:
                tree.add(f'{a}: {val.__name__}')
        return tree


class AtItem[T](ReadableClass):
    
    def __init__(self, original, schema:Schema[T]):
        super().__init__()
        self.original = original
        self.schema = schema
    
    @property
    def accessors(self) -> Generator['Accessor']:
        for a in self.schema.accessors:
            yield a.prepend('@idx')
    
    def _root_repr(self):
        return f'@idx: {self.schema.root.__name__}'
    
    def _tree(self, tree):
        return self.schema._tree(tree)
