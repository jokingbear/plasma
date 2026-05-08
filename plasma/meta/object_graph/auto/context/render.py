import re

from inspect import _empty
from rich.console import Console
from rich.tree import Tree
from typing import get_args

from ..context_graph import ContextGraph, Node
from .....functional.helpers.color_printer import Color


def render_context(graph:ContextGraph, context):
    rendered = set()
    root = Tree(context)
    for node_name in graph.inquirer.node_names(context):
        node_id = context, node_name
        if graph.inquirer.context_in_degree(node_id) == 0:
            render_node(graph, node_id, root, rendered)

    console =  Console(force_jupyter=False, force_terminal=True)
    with console.capture() as capture:
        console.print(root)
    return capture.get()


def render_node(graph:ContextGraph, node, tree:Tree, rendered:set):
    _, node_name = node
    if isinstance(node_name, tuple):
        node_name = str(node_name[-1])
    else:
        node_name = str(node_name)

    node_type = graph.inquirer.type(node)
    value, = graph.inquirer.select(node, 'value')
    expansion = True
    
    if node in rendered and node_type is not Node.LEAF:
        node_name += '...'
        expansion = False
    elif node_type is Node.FACTORY:
        node_name += ':Factory'
    elif node_type is Node.LEAF:
        if value is not _empty:
            node_name += f':{render_type(value)}' # type:ignore
        node_name = f'[red]{node_name}[/red]'
    elif node_type is Node.SINGLETON:
        node_name += f'={render_type(type(value))}'
        node_name = f'[yellow]{node_name}[/yellow]'
    elif node_type is Node.DELEGATE:
        linked_node, = graph.successors(node)
        linked_context, linked_name = linked_node
        linked_name = f'{linked_name}:{linked_context}'
        node_name = f'[blue]{node_name} --> {linked_name}[/blue]'
        expansion = False
    
    tree = tree.add(node_name)
    
    if expansion:
        for m in graph.successors(node):
            render_node(graph, m, tree, rendered)

    rendered.add(node)


def render_type(t:type):
    type_str = repr(t)
    type_str = re.sub(r'[\w_]+\.', '', type_str)
    type_str = re.sub(r'<class \'(.+?)\'>', r'\1', type_str)
    type_str = type_str.replace('[', '\\[')
    return type_str
