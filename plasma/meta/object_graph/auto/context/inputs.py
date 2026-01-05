from ..context_graph import Node, ContextGraph
from .require import Require


class InputDict(dict):
    
    def __init__(self, graph:ContextGraph, context, names:list[str]):
        super().__init__()
        
        for n in names:
            node_id = context, n
            drill_down(graph, node_id, self)
    
    def __repr__(self):
        lines = ['{']
        for k, v in self.items():
            lines.append(f'  {k}: {type(v).__name__}')
        lines.append('}')
        return '\n'.join(lines)


def drill_down(graph:ContextGraph, node, objects:dict):
    node_name = node[1]
    node_type = graph.inquirer.type(node)
    
    match node_type:
        case Node.LEAF:
            objects[node_name] = Require()
        case Node.SINGLETON:
            value, = graph.inquirer.select(node, 'value')
            objects[node_name] = value
        case Node.DELEGATE:
            linked_node, = graph.successors(node)
            new_context, _ = linked_node
            new_object_dict = {}
            objects[new_context] = new_object_dict
            drill_down(graph, linked_node, new_object_dict)
        case Node.INITIATOR|Node.FACTORY:
            for n in graph.successors(node):
                drill_down(graph, n, objects)
