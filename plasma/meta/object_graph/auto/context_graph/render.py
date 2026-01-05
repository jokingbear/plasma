import networkx as nx

from .meta import Meta
from .types import Node
from inspect import _empty
from typing import get_args


def render(meta:Meta, graph:nx.DiGraph):
    sorted_contexts = sorted(meta, key=str)
    
    lines = []
    for context in sorted_contexts:
        contexted_graph = graph.subgraph((context, n) for n in meta[context])
        lines.append(f'{context}:')
        lines.extend('\t' + l for l in render_context(contexted_graph))
        lines.append('=' * 50)
    
    return '\n'.join(lines)
        

def render_context(graph:nx.DiGraph):
    lines = []
    rendered = set()
    for n in graph:
        if graph.in_degree(n) == 0:
            indent = ''
            render_node(graph, n, indent, lines, rendered)
    return lines


def render_node(graph:nx.DiGraph, node, indent:str, lines:list, rendered:set):
    line = f'{indent}|->{node[1]}'
    
    if node in rendered:
        line += '...'
        lines.append(line)
        return
    
    node_type, value = graph.inquirer.select(node, 'type', 'value')
    if node_type is Node.LEAF and value is not _empty:
        line += f':{render_type(value)}'
    elif node_type is Node.SINGLETON:
        line += f'={render_type(type(value))}'
    
    lines.append(line)
    
    for m in graph.successors(node):
        new_indent = indent + ' ' * 2
        render_node(graph, m, new_indent, lines, rendered)

    rendered.add(node)


def render_type(t:type):
    generic_args = get_args(t)
    
    if hasattr(t, '__name__'):
        name = t.__name__
    else:
        name = 'Union'
    
    if len(generic_args) == 0:
        return name
    else:
        generic_arg_texts = []
        for a in generic_args:
            if isinstance(a, list):
                rendered_args = [render_type(g) for g in a]
                generic_arg_texts.append('[' + ', '.join(rendered_args) + ']')
            else:
                generic_arg_texts.append(render_type(a))
        generic_arg_texts = ','.join(generic_arg_texts)
        return f'{name}[{generic_arg_texts}]' 
