import re
import networkx as nx

from typing import Callable

from .accessor import AccessorInitGraph
from .initiator import Initator
from .struct import StructInitGraph
from ..schemas import schema
from ....functional import ReadableClass


class Parser[T](ReadableClass):
    
    def __init__(self, cls:type[T], 
                 type_parser:dict[type, Callable[[object], object]]={}):
        super().__init__()
        
        self.cls = cls
        self._schema = schema(cls)
        self.type_parser = type_parser
    
    def from_accessors(self, accessors:dict[str, object]) -> T:
        graph = AccessorInitGraph(accessors)
        self._parse(graph)
        return Initator(self._schema.rep, graph, self._schema.real_to_rep).run()
    
    def from_struct(self, struct:dict) -> T:
        graph = StructInitGraph(self._schema.rep, struct, self._schema.real_to_rep)
        self._parse(graph)
        return Initator(self._schema.rep, graph, self._schema.real_to_rep).run()

    def _parse(self, graph:nx.DiGraph):
        for n in graph:
            if graph.out_degree(n) == 0: 
                value = graph.nodes[n]['value']
                rep_node = self._schema.real_to_rep(n)
                origin = self._schema.rep.origin(rep_node)
                parser = self.type_parser.get(origin, lambda x:x)
                
                try:
                    value = parser(value)
                except Exception as e:
                    error = AttributeError(value)
                    accessor = '.'.join(str(a) for a in n)
                    error.add_note(f'error parsing {value} at {accessor}')
                
                graph.add_node(n, value=value)