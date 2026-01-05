from ..context_graph import Node, ContextGraph
from .require import Require
from .....functional.helpers.color_printer import Color


class InputDict(dict):
    
    def __init__(self, graph:ContextGraph, context, names:list[str]):
        super().__init__()
        
        inquirer = graph.inquirer
        inputs = {c: {} for c in inquirer.list_context()}
        for n in names:
            node_id = context, n
            drill_down(graph, node_id, inputs)
        self.update(inputs[context])
        self.update({i:data for i, data in inputs.items() if i != context and len(data) > 0})
    
    def __repr__(self):
        lines = ['{']
        render(self, ' ' * 2, lines)
        lines.append('}')
        return '\n'.join(lines)


def drill_down(graph:ContextGraph, node, objects:dict):
    context, node_name = node
    node_type = graph.inquirer.type(node)
    
    match node_type:
        case Node.LEAF:
            objects[context][node_name] = Require()
        case Node.SINGLETON:
            value, = graph.inquirer.select(node, 'value')
            objects[context][node_name] = value
        case Node.DELEGATE:
            linked_node, = graph.successors(node)
            drill_down(graph, linked_node, objects)
        case Node.INITIATOR|Node.FACTORY:
            for n in graph.successors(node):
                drill_down(graph, n, objects)


def render(data:dict, indent:str, lines:list):
    for k, v in data.items():
        if '.' in k:
            lines.append(f'{indent}{k}:{{')
            render(data[k], indent + '\t', lines)
            lines.append(f'{indent}}}')
        else:
            value = v
            if isinstance(v, Require):
                value = Color.RED.render(Require.__name__)
            else:
                value = Color.BLUE.render(type(v).__name__)

            lines.append(f'{indent}{k}: {value}')
