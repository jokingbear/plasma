import networkx as nx

from typing import Any
from .sub_indexes import NodeSubIndex, EdgeSubindex
from .node_editor import NodeEditor
from .edge_editor import EdgeEditor
from .inquirer import Inquirer
from ...object_inquirer import ObjectInquirer
from ....base_model import Field


class Index:
    
    def __init__(self, graph:nx.DiGraph, named_indices:dict[str, Any]):        
        self.graph = graph
        
        indices = dict(
            (name, NodeSubIndex(AttributeSelector(graph, 'data', selector)))
            for name, selector in named_indices.items()
        )
        
        type_index_name = 'type'
        indices.setdefault(type_index_name, NodeSubIndex(AttributeSelector(graph, 'type')))  
        
        self.type_index_name = type_index_name
        self._indices = indices
        self._successors = EdgeSubindex(AttributeSelector(graph, type_index_name))
        self._predecessors = EdgeSubindex(AttributeSelector(graph, type_index_name))
    
    @property
    def node_editor(self):
        return NodeEditor(
            self.graph, 
            self._indices.values(), 
            self.edge_editor
        )
    
    @property
    def edge_editor(self):
        return EdgeEditor(self.graph, self._successors, self._predecessors)
    
    @property
    def inquirer(self):
        return Inquirer(
            self.graph, self._indices, 
            self._successors, self._predecessors,
            self.type
        )

    def type(self, node_id):
        return self.graph.nodes[node_id]['type']

    def data(self, node_id):
        return self.graph.nodes[node_id]['data']

    @property
    def names(self):
        return [k for k in self._indices if k != 'type']


class AttributeSelector:
    
    def __init__(self, graph:nx.DiGraph, prefix:str, attr:str|Field|None=None) -> None:
        self.graph = graph
        self.prefix = prefix
        self.attr = attr
    
    def __call__(self, node_id) -> Any:
        data = self.graph.nodes[node_id][self.prefix]
        if self.attr is None:
            return data
        
        inquirer = ObjectInquirer(data)
        value = inquirer.get(self.attr, default=None)
        return value
