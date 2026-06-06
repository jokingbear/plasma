import networkx as nx

from typing import Callable, Optional, Any
from types import UnionType

from .accessor import AccessorInitGraph
from .initiator import Initator
from .struct import StructInitGraph
from ..schemas import schema
from ....functional import ReadableClass


class Parser[T](ReadableClass):
    
    def __init__(
            self, cls:type[T], 
            type_parser:dict[type, Callable[[Any], Any]]={}
        ):
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
        exceptions = []
        for n in graph:
            if graph.out_degree(n) > 0:
                continue 
            
            value = graph.nodes[n]['value']
            if value is None:
                continue
            
            rep_node = self._schema.real_to_rep(n)
            raw = self._schema.rep.raw(rep_node)
            origin, args = self._schema.rep.type(rep_node)
            try:
                if raw in self.type_parser:
                    value = self.type_parser[raw](value)
                elif origin is UnionType:
                    value = self._parse_union(value, args)
                elif origin is Optional and len(args) > 0 and args[0] in self.type_parser:
                    value = self.type_parser[args[0]](value)
                elif origin in self.type_parser:
                    value = self.type_parser[origin](value) #type:ignore - incorrect check

                graph.add_node(n, value=value)
            except Exception as e:
                accessor = '.'.join(str(a) for a in n)
                e.add_note(f'error parsing {value} at {accessor}')
                exceptions.append(e)
        
        if len(exceptions) > 0:
            raise ExceptionGroup('error parsing data', exceptions)

    def _parse_union(self, value, args):
        exceptions = []
        temp_value = InitValue
        for a in args:
            if a not in self.type_parser:
                continue

            try:
                temp_value = self.type_parser[a](value)
                break
            except Exception as e:
                exceptions.append(e)
        
        if temp_value is InitValue and len(exceptions) > 0:
            e = ExceptionGroup('cannot find a valid parser', exceptions)
            raise e
        
        return temp_value if temp_value is not InitValue else value


class InitValue:...
