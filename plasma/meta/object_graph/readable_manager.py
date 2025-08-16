import typing
import networkx as nx

from .factorial_manager import FactoryManager


class ReadableManager(FactoryManager):
    
    def __repr__(self):
        lines = []
        rendered = set()
        for r in self._dep_graph:
            if self._dep_graph.in_degree(r) == 0:
                _render_node(self._dep_graph, r, '', lines, rendered)
                lines.append('-' * 100)
        text = '\n'.join(lines)
        return text

    @property
    def entries(self):
        leaves = {}
        for n, val in self._dep_graph.nodes(data='value', default=NotInitalized):
            if self._dep_graph.out_degree(n) == 0:
                leaves[n] = val
        
        return leaves


class NotInitalized:
    pass


def _render_node(graph:nx.DiGraph, key, prefix:str, lines:list, rendered:set):
    node = graph.nodes[key]
    if key in rendered and graph.out_degree(key) > 0:
        lines.append(f'{prefix}|->{key}...')
    elif 'value' in node:
        lines.append(f'{prefix}|->{key} = {render_annotation(type(node['value']))}')
    else:
        if 'factory' in node:
            lines.append(f'{prefix}|->{key}: {type(node['factory']).__name__}')
        elif 'annotation' in node:
            lines.append(f'{prefix}|->{key}: {render_annotation(node['annotation'])}')
        else:
            lines.append(f'{prefix}|->{key}')

        for n in graph.neighbors(key):
            _render_node(graph, n, prefix + ' ' * 2, lines, rendered)
    rendered.add(key)


def render_annotation(t:type):
    generic_args = typing.get_args(t)
    
    if hasattr(t, '__name__'):
        name = t.__name__
    else:
        name = 'UnionType'
    
    if len(generic_args) == 0:
        return name
    else:
        generic_arg_texts = []
        for a in generic_args:
            if isinstance(a, list):
                rendered_args = [render_annotation(g) for g in a]
                generic_arg_texts.append('[' + ', '.join(rendered_args) + ']')
            else:
                generic_arg_texts.append(render_annotation(a))
        generic_arg_texts = ','.join(generic_arg_texts)
        return f'{name}[{generic_arg_texts}]' 
