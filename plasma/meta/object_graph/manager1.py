import inspect
import networkx as nx
import re
import pandas as pd

from ...functional import AutoPipe
from .injector import DependencyInjector


class Manager(AutoPipe):

    def __init__(self):
        super().__init__()

        self._dep_graph = nx.DiGraph()

    def run(self, *names, **init_args) -> dict:
        results = DependencyInjector(self._dep_graph).run(*names, **init_args)
        return results
    
    def add_dependency(self, name, value, as_singleton=False):
        assert as_singleton or callable(value), 'depdency should be callable'
        
        if name in self._dep_graph:
            neighbors = [*self._dep_graph.neighbors(name)]
            self._dep_graph.remove_edges_from([(name, n) for n in neighbors])
        
        if as_singleton:
            self._dep_graph.add_node(name, value=value)    
        else:
            self._dep_graph.add_node(name, initiator=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    self._dep_graph.add_node(arg_name)
                    self._dep_graph.add_edge(name, arg_name)
                    
                    if p.default is not inspect.Parameter.empty:
                        self._dep_graph.add_node(arg_name, value=p.default)

        return self

    def merge(self, injector):
        assert isinstance(injector, DependencyInjector), 'injector must be an DependencyInjector instance'
        self._dep_graph = nx.compose(self._dep_graph, injector._dep_graph)

        return self

    def duplicate(self, current_name:str, new_name:str):
        assert current_name in self._dep_graph, 'current name must be in dep graph'
        assert new_name not in self._dep_graph, 'new name must not be in dep graph'
        
        node = self._dep_graph.nodes[current_name]
        neighbors = [*self._dep_graph.successors(current_name)]
        self._dep_graph.add_node(new_name, **node)
        for n in neighbors:
            self._dep_graph.add_edge(new_name, n)
        
        return self

    def __repr__(self):
        lines = []
        prefix = '|'
        indent = '--'
        for r in self._dep_graph:
            if self._dep_graph.in_degree(r) == 0:
                lines.append(_render_node(self._dep_graph, r, prefix, indent))
                lines.append('-' * 100)
        text = '\n'.join(lines)
        pattern = f'{prefix}{indent}'.replace('|', r'\|')
        text = re.sub(rf'({pattern}){{1,}}', lambda m: m.group(0).replace(prefix + indent, ' ' * (len(indent) + 1)) + prefix + indent, text)
        return text


def _render_node(graph:nx.DiGraph, key, prefix='|', indent=' ' * 2):
    node = graph.nodes[key]
    if 'value' in node:
        lines = [f'{key}={type(node["value"])}']
    else:
        lines = [key]
        for n in graph.neighbors(key):
            rendered_lines = _render_node(graph, n, prefix, indent)
            rendered_lines = rendered_lines.split('\n')
            rendered_lines = [prefix + indent + t for t in rendered_lines]
            lines.extend(rendered_lines)
    
    return '\n'.join(lines)
