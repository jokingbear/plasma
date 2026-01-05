import networkx as nx

from inspect import _empty
from typing import get_args
from ..context_graph import ContextGraph, Node
from .....functional.helpers.color_printer import Color


def render_context(graph:ContextGraph, context):
    lines = []
    rendered = set()
    for node_name in graph.inquirer.nodes(context):
        node_id = context, node_name
        if graph.in_degree(node_id) == 0:
            indent = ''
            render_node(graph, node_id, indent, lines, rendered)
    return '\n'.join(lines)


def render_node(graph:ContextGraph, node, indent:str, lines:list, rendered:set):
    node_name = node[1]
    node_type = graph.inquirer.type(node)
    value, = graph.inquirer.select(node, 'value')
    
    if node in rendered and node_type is not Node.LEAF:
        node_name += '...'
    elif node_type is Node.FACTORY:
        node_name += ':Factory'
    elif node_type is Node.LEAF and value is not _empty:
        node_name += f':{render_type(value)}'
        node_name = Color.RED.render(node_name)
    elif node_type is Node.SINGLETON:
        node_name += f'={render_type(type(value))}'
        node_name = Color.YELLOW.render(node_name)
    elif node_type is Node.DELEGATE:
        node_name = Color.BLUE.render(node_name)
    
    line = f'{indent}|->{node_name}'
    lines.append(line)
    
    if node_type is Node.DELEGATE:
        pass
    else:
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
