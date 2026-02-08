import itertools
import networkx as nx

from ..index import Index
from ...object_inquirer import ObjectInquirer, TupleDict
from typing import Callable, Hashable, Iterator


class Nodes:
    
    def __init__(self, 
                index:Index, 
                ids:Iterator[Hashable],
                attributes:set[Hashable]=(),
                selector_funcs:dict[str, Callable[[Hashable, nx.DiGraph], object]]={},
                default=None,
            ):

        self._ids = ids
        self._index = index
        self._attributes = set(attributes)
        self._select_funcs = selector_funcs
        self._default = default
    
    def select(self, *attributes:Hashable, default=None, override=True,
                **select_funcs:Callable[[Hashable, nx.DiGraph], object],
            ):
        new_iterable = self._clone()
        new_attributes = set(attributes) if override else self._attributes.union(attributes)
        new_selectors = select_funcs if override else {**select_funcs, **self._select_funcs}
        return Nodes(self._index, new_iterable, new_attributes, new_selectors, default)

    def filter(self, *predicates:Callable[[Hashable, TupleDict], bool]):
        new_iterator = self._clone()
        new_iterator = (
            (i, ObjectInquirer(self._index.data(i)).select(self._attributes)) 
            for i in self._ids
        )
        
        new_iterator = (i for i, data in new_iterator if all(p(i, data) for p in predicates))
        return Nodes(self._index, new_iterator, self._attributes, self._default)
    
    def unwind[V](self, list_func:Callable[[Hashable, TupleDict], Iterator[V]]):
        for i in self._clone():
            data = ObjectInquirer(self._index.data(i)).select(self._attributes)
            for new_value in list_func(i, data):
                yield new_value
    
    def accumulate[V](self, 
                      initial:V, func:Callable[[V, Hashable, TupleDict], V|None], 
                      stateful=True # check if func update intial V
                ) -> V:
        running_value = initial
        for i in self._clone():
            data_inquirer = ObjectInquirer(self._index.data(i))
            selected_data = data_inquirer.select(self._attributes, self._default)
            new_running_value = func(running_value, i, selected_data)
            if not stateful:
                running_value = new_running_value
        
        return running_value
    
    def __iter__(self):
        for i in self._clone():
            if len(self._attributes) > 0:
                data_inquirer = ObjectInquirer(self._index.data(i))
                data = data_inquirer.select(self._attributes, self._default)
                additional_data = {n: f(i, self._index.graph) for n, f in self._select_funcs.items()}
                final_data = data.update(additional_data)
                yield i, *final_data
            else:
                yield i

    def _clone(self):
        iterator1, iterator2 = itertools.tee(self._ids)
        self._ids = iterator1
        return iterator2
