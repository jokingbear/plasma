import itertools

from ..index import Index
from typing import Callable, Hashable, Iterator
from ...object_inquirer import ObjectInquirer, TupleDict


class Nodes:
    
    def __init__(self, 
                index:Index, 
                ids:Iterator[Hashable],
                attributes:set[Hashable]=(),
                default=None,
            ):

        self._ids = ids
        self._index = index
        self.attributes = set(attributes)
        self.default = default
    
    def select(self, *attributes:Hashable, default=None, override=True):
        new_iterable = self._clone()
        new_attributes = set(attributes) if override else self.attributes.union(attributes)
        return Nodes(self._index, new_iterable, new_attributes, default)

    def filter(self, *predicates:Callable[[Hashable, TupleDict], bool]):
        new_iterator = self._clone()
        new_iterator = (
            (i, ObjectInquirer(self._index.data(i)).select(self.attributes)) 
            for i in self._ids
        )
        
        new_iterator = (i for i, data in new_iterator if all(p(i, data) for p in predicates))
        return Nodes(self._index, new_iterator, self.attributes, self.default)
    
    def unwind[V](self, list_func:Callable[[Hashable, TupleDict], Iterator[V]]):
        for i in self._clone():
            data = ObjectInquirer(self._index.data(i)).select(self.attributes)
            for new_value in list_func(i, data):
                yield new_value
    
    def accumulate[V](self, 
                      initial:V, func:Callable[[V, Hashable, TupleDict], V], 
                      stateful=True
                ) -> V:
        running_value = initial
        for i in self._clone():
            data_inquirer = ObjectInquirer(self._index.data(i))
            selected_data = data_inquirer.select(self.attributes, self.default)
            new_running_value = func(running_value, i, selected_data)
            if not stateful:
                running_value = new_running_value
        
        return running_value
    
    def __iter__(self):
        for i in self._clone():
            if len(self.attributes) > 0:
                data_inquirer = ObjectInquirer(self._index.data(i))
                yield i, *data_inquirer.select(self.attributes, self.default)
            else:
                yield i

    def _clone(self):
        iterator1, iterator2 = itertools.tee(self._ids)
        self._ids = iterator1
        return iterator2
