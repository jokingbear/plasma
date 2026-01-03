import networkx as nx

from .meta import Meta
from .types import Node
from inspect import _empty


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
    node_type, value = graph.inquirer.select(node, 'type', 'value')
    if node_type is Node.LEAF and value is not _empty:
        line += f':{value.__name__}'
    elif node_type is Node.SINGLETON:
        line += f'={type(value).__name__}'
    
    lines.append(line)
    
    for m in graph.successors(node):
        if m not in rendered:
            new_indent = indent + ' ' * 2
            render_node(graph, m, new_indent, lines, rendered)

    rendered.add(node)
