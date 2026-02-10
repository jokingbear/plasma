import itertools
import networkx as nx

from ..index import Index
from ...object_inquirer import ObjectInquirer, TupleDict
from typing import Callable, Hashable, Iterator
from .....functional.helpers import groupby, auto_map

SelectFunc = Callable[[Hashable, nx.DiGraph], object]


class Nodes:
    
    def __init__(self, 
                index:Index, 
                ids:Iterator[Hashable],
                attributes:tuple[Hashable]=(),
                selector_funcs:tuple[tuple[str, SelectFunc]]=(),
                default=None,
            ):

        self._ids = ids
        self._index = index
        self._attributes = attributes
        self._select_funcs = selector_funcs
        self._default = default
    
    def select(self, *attributes:Hashable, default=None, override=True,
                **select_funcs:Callable[[Hashable, nx.DiGraph], object],
            ):
        assert len(set(attributes)) == len(attributes), 'attributes name must be unique'
        
        new_iterable = self._clone()
        new_attributes = attributes if override else self._attributes.union(attributes)

        new_selectors = tuple(select_funcs.items()) if override \
                        else [*self._select_funcs, *select_funcs.items()]
        return Nodes(self._index, new_iterable, new_attributes, new_selectors, default)

    def filter(self, *predicates:Callable[[Hashable, TupleDict], bool]):
        new_iterator = self._tuple_iter()        
        new_iterator = (i for i, data in new_iterator if all(p(i, data) for p in predicates))
        return Nodes(self._index, new_iterator, self._attributes, self._default)
    
    def unwind[V](self, list_func:Callable[[Hashable, TupleDict], Iterator[V]]):
        for i, data in self._tuple_iter():
            for new_value in list_func(i, data):
                yield new_value
    
    def accumulate[V](self, 
                      initial:V, func:Callable[[V, Hashable, TupleDict], V|None], 
                      stateful=True # check if func update intial V
                ) -> V:
        running_value = initial
        for i, data in self._tuple_iter():
            new_running_value = func(running_value, i, data)
            if not stateful:
                running_value = new_running_value
        
        return running_value

    def groupby[T](self, key:Callable[[Hashable, TupleDict], T]):
        return groupby[T, Hashable](self._tuple_iter(), auto_map(key), lambda key_data:key_data[0])
    
    def __iter__(self):
        for nid, data in self._tuple_iter():
            if len(data) > 0:
                yield nid, *data
            else:
                yield nid

    def _tuple_iter(self):
        for i in self._clone():
            data_inquirer = ObjectInquirer(self._index.data(i))
            data = data_inquirer.select(self._attributes, self._default)
            additional_data = [(n, f(i, self._index.graph)) for n, f in self._select_funcs]
            final_data = data.update(
                [n for n, _ in additional_data],
                [d for _, d in additional_data]
            )
            yield i, final_data
    
    def _clone(self):
        iterator1, iterator2 = itertools.tee(self._ids)
        self._ids = iterator1
        return iterator2
