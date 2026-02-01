import itertools

from ..index import Index
from .....functional import auto_map
from typing import Callable, Hashable, Iterable, Self
from ...object_inquirer import ObjectInquirer


class Nodes(Iterable[Hashable|tuple]):
    
    def __init__(self, 
                index:Index, 
                ids:Iterable[Hashable],
                attributes:set[Hashable],
                default
            ):

        self._ids = ids
        self._index = index
        self.attributes = set(attributes)
        self.default = default
    
    def select(self, *attributes:Hashable, default=None, override=True):
        iterable1, iterable2 = itertools.tee(self.ids)
        self._ids = iterable1
        new_attributes = set(attributes) if override else self.attributes.union(attributes)
        return Nodes(self._index, iterable2, new_attributes, default)

    def filter(self, *predicates:Callable[[Hashable, dict], bool]):
        iterable1, iterable2 = itertools.tee(self.ids)
        iterable2 = (
            (i, ObjectInquirer(self._index.data(i)).select(self.attributes)) for i in self._ids
            if all(p(i, {}) if len(self.attributes) == 0 
                   else None for p in predicates)
        )
        iterable2 = (i for i, data in iterable2 if all(p(i, data) for p in predicates))
        self._ids = iterable1
        return Nodes(self._index, iterable2, self.attributes, self.default)
    
    def unwind[V](self, list_func:Callable[[Hashable, dict], Iterable[V]]) -> Iterable[V]:
        pass
    
    def accumulate[V](self, initial:V, func:Callable[[V, Hashable, dict], V]) -> V:
        running_value = initial
        for i in self._ids:
            data_inquirer = ObjectInquirer(self._index.data(i))
            selected_data = data_inquirer.select(self.attributes, self.default)
            running_value = func(running_value, i, selected_data)
        
        return running_value
    
    def __iter__(self):
        for i in self._ids:
            if len(self.attributes) > 0:
                data_inquirer = ObjectInquirer(self._index.data(i))
                yield i, *data_inquirer.select(self.attributes, self.default)
            else:
                yield i
