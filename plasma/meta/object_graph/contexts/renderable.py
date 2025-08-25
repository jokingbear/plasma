import typing
import networkx as nx

from .factorial import FactorialContext
from ..types import Node


class RenderableContext(FactorialContext):
    
    def __repr__(self):
        lines = []
        rendered = set()
        for n in self.graph.neighbors(self.name):
            if self.graph.in_degree(n) == 1:
                lines.append(self.name)
                _render_node(self.graph, self.name, n, '  ', lines, rendered)
                lines.append('-' * 100)
        text = '\n'.join(lines)
        return text


def _render_node(graph:nx.DiGraph, current_context, key, prefix:str, lines:list, rendered:set):
    node_attr = graph.nodes[key]
    node_type = node_attr.get('type', Node.LEAF)
    
    context, name = key
    if context != current_context:
        lines.append(f'{prefix}|->{context}.{name}')
        if graph.out_degree(key) > 0:
            lines[-1] += '...'
    elif key in rendered:
        lines.append(f'{prefix}|->{name}')
        
        if graph.out_degree(key) > 0:
            lines[-1] += '...'
    elif node_type is Node.SINGLETON:
        lines.append(f'{prefix}|->{name} = {render_annotation(type(node_attr['value']))}')
    else:
        if node_type is Node.FACTORY:
            lines.append(f'{prefix}|->{name}: {type(node_attr['value']).__name__}')
        elif 'annotation' in node_attr:
            lines.append(f'{prefix}|->{name}: {render_annotation(node_attr['annotation'])}')
        else:
            lines.append(f'{prefix}|->{name}')

        for n in graph.neighbors(key):
            _render_node(graph, current_context, n, prefix + ' ' * 2, lines, rendered)
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
