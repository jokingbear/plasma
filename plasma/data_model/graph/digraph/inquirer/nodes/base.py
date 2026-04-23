import itertools

from typing import Any, Callable, Hashable, Iterable

from .projector import Projector
from .tuple_dict import TupleDict
from .utils import compile, select_node
from ...index import Index
from ....object_inquirer import ObjectInquirer
from .....base_model import Field
from .....collections import groupby, Stream
from ......functional.helpers import auto_map

Selector = (
    Callable[[Hashable], object]
    |Callable[[Hashable, Any], object]
    |Callable[[Hashable, Any, TupleDict], object]
)


class Nodes[T:Hashable|tuple[Hashable, TupleDict]](Iterable[T]):
    
    def __init__(
            self, 
            index:Index, 
            ids:Iterable[Hashable],
            projector:Projector[T],
        ):

        self._ids = ids
        self._index = index
        self._projector = projector
    
    def node_ids(self):
        return Nodes(self._index, self._ids, self._projector.update([], [], None, False))
    
    def select(
            self, 
            *attributes:str|Field, 
            default=None, override=True,
            **selectors:(
                str|Field
                |Callable[[Hashable], object]
                |Callable[[Hashable, T], object]
                |Callable[[Hashable, T, TupleDict], object]
            ),
        ):
        assert len(set(attributes)) == len(attributes), 'attributes name must be unique'
        compiled_selectors = []
        for n, s in selectors.items():
            s = compile(type(self._projector.inquirer), s)
            compiled_selectors.append((n, s))
        
        projector = self._projector.update(attributes, compiled_selectors, default, override)
        return Nodes(self._index, self._clone(), projector)

    def filter(self, *predicates:Callable[[Hashable, TupleDict], bool]):
        new_iterator = self._tuple_iter()        
        new_iterator = (i for i, data in new_iterator if all(p(i, data) for p in predicates))
        return Nodes(self._index, new_iterator, self._projector)
    
    def unwind[V](self, list_func:Callable[[Hashable, TupleDict], Iterable[V]]):
        return Stream.from_iterable(list_func(i, data) for i, data in self._tuple_iter())
    
    def accumulate[K, V](
            self, 
            initial:V, 
            selector:Callable[[Hashable, TupleDict], K],
            accumulator:Callable[[V, K], V|None], 
            stateful=True # check if func update intial V
        ) -> V:
        running_value = initial
        for i, data in self._tuple_iter():
            accumulating_value = selector(i, data)
            new_running_value = accumulator(running_value, accumulating_value)
            if not stateful and new_running_value is not None:
                running_value = new_running_value
        
        return running_value

    def groupby[K, V](
            self,
            key:Callable[[Hashable, TupleDict], K],
            value:Callable[[Hashable, TupleDict], V]=select_node,
        ):
        value = value or (lambda n,_: n)
        return groupby[K, V](self._tuple_iter(), auto_map(key), auto_map(value))
    
    def __iter__(self):
        for nid, data in self._tuple_iter():
            if len(data) == 0:
                yield nid
            else:
                yield nid, *data

    def _tuple_iter(self):
        for nid in self._clone():
            data_inquirer = ObjectInquirer(self._index.data(nid))
            qresults = self._projector(nid, data_inquirer)
            yield nid, qresults
    
    def _clone(self):
        iterator1, iterator2 = itertools.tee(self._ids)
        self._ids = iterator1
        return iterator2
