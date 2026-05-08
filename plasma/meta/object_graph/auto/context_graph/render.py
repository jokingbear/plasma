import networkx as nx

from inspect import _empty
from rich.tree import Tree
from rich.console import Console
from typing import get_args
from .inquirer import Inquirer
from .meta import Meta
from .types import Node


def render(meta:Meta, graph:nx.DiGraph, inquirer:Inquirer):
    sorted_contexts = sorted(meta, key=str)
    
    lines = []
    for context in sorted_contexts:
        context_repr = render_context(graph, inquirer, context)
        lines.append(context_repr)
    
    return '\n'.join(lines)
        

def render_context(graph:nx.DiGraph, inquirer:Inquirer, context):
    rendered = set()
    root = Tree(context)
    for n in inquirer.node_names(context):
        node_id = context, n
        if inquirer.context_in_degree(node_id) == 0:
            render_node(graph, inquirer, node_id, root, rendered)
    
    console = Console(force_jupyter=False, force_terminal=True)
    with console.capture() as capture:
        console.print(root)
    return capture.get()


def render_node(graph:nx.DiGraph, inquirer:Inquirer, node, tree:Tree, rendered:set):
    _, node_name = node
    if isinstance(node_name, tuple):
        node_name = str(node_name[-1])
    else:
        node_name = str(node_name)

    node_type = inquirer.type(node)
    value, = inquirer.select(node, 'value')
    expand = True
    
    if node in rendered and node_type is not Node.LEAF:
        node_name += '...'
        expand = False
    elif node_type is Node.FACTORY:
        node_name += ':Factory'
    elif node_type is Node.LEAF and value is not _empty:
        node_name += f':{render_type(value)}' #type:ignore
    elif node_type is Node.SINGLETON:
        node_name += f'={render_type(type(value))}'
    elif node_type is Node.DELEGATE:
        linked_node, = graph.successors(node)
        linked_context, linked_name = linked_node
        node_name += f' --> {linked_name}:{linked_context}'
        expand = False

    tree = tree.add(node_name)
    
    if expand:
        for m in graph.successors(node):
            render_node(graph, inquirer, m, tree, rendered)

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
        
        if name == 'Union':
            return '|'.join(generic_arg_texts)
        else:
            generic_arg_texts = ','.join(generic_arg_texts)
            return f'{name}[{generic_arg_texts}]' 
