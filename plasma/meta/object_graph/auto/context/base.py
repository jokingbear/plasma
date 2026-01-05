import pandas as pd

from .....functional import AutoPipe
from ..context_graph import ContextGraph, Node
from pathlib import Path
from .render import render_context


class Context(AutoPipe):
    
    def __init__(self, graph:ContextGraph, context:Path):
        super().__init__()
        
        self.name = context
        self.graph = graph
    
    def run(self, *inputs:str, **kwargs):
        assert len(inputs) > 0
        
        results = {**kwargs}
        for i in inputs:
            init_object(self.graph, (self.name, i), results)

        return pd.Series({i: results[self.name, i] for i in inputs}).loc[inputs]

    def __repr__(self):
        return render_context(self.graph, self.name)


def init_object(graph:ContextGraph, node, initiated_objects:dict):
    if node not in initiated_objects:
        node_type = graph.inquirer.type(node)
        context, node_name = node

        if node_type is Node.SINGLETON:
            initiated_objects[node], = graph.inquirer.select(node, 'value')
        elif node_type is Node.LEAF:
            context, node_name = node
            raise ReferenceError(f'there is no input value for {node_name} in {context}')
        elif node_type is Node.FACTORY:
            factory = {}
            for m in graph.successors(node):
                init_object(graph, m, initiated_objects)
                _, child_name = m
                factory[child_name] = initiated_objects[m]
            initiated_objects[node] = factory
        elif node_type is Node.DELEGATE:
            delegated_node, = graph.successors(node)
            init_object(graph, delegated_node, initiated_objects)
            initiated_objects[node] = delegated_node
        else:
            args = {}
            for m in graph.successors(node):
                init_object(graph, m, initiated_objects)
                _, child_name = m
                args[child_name] = initiated_objects[m]
            initiator, = graph.inquirer.select(node, 'value')
            initiated_objects[node] = initiator(**args)
