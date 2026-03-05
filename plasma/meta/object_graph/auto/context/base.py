import pandas as pd

from .....functional import AutoPipe
from ..context_graph import ContextGraph, Node
from .render import render_context
from .inputs import InputDict


class Context(AutoPipe):
    
    def __init__(self, graph:ContextGraph, context:str):
        super().__init__()
        
        graph.init_context(context)
        self.name = context
        self.graph = graph
    
    def run(self, *inputs:str, **kwargs):
        assert len(inputs) > 0
        
        global_vars = {k: v for k, v in kwargs.items() if '.' not in k}
        context_vars = {k: v for k,v in kwargs.items() if '.' in k}
        for c in self.graph.inquirer.list_context():
            if c not in context_vars:
                context_vars[c] = {}

        context_vars[self.name] = global_vars
        type_caches = {}
        for i in inputs:
            init_object(self.graph, (self.name, i), context_vars, global_vars, type_caches)

        return pd.Series({i: context_vars[self.name][i] for i in inputs}).loc[list(inputs)]

    def inputs(self, *names):
        return InputDict(self.graph, self.name, names)
    
    def __repr__(self):
        return render_context(self.graph, self.name)


def init_object(graph:ContextGraph, node, context_vars:dict, global_vars:dict, type_cache:dict):
    context, node_name = node
    if node_name not in context_vars[context]:
        node_type = graph.inquirer.type(node)
        context, node_name = node

        if node_name in global_vars:
            obj = global_vars[node_name]
        elif node_type is Node.SINGLETON:
            obj, = graph.inquirer.select(node, 'value')
        elif node_type is Node.LEAF:
            raise ReferenceError(f'there is no input value for {node_name} in {context}')
        elif node_type is Node.FACTORY:
            obj = {}
            for m in graph.successors(node):
                init_object(graph, m, context_vars, global_vars, type_cache)
                child_context, child_name = m
                obj[child_name[1]] = context_vars[child_context][child_name]
        elif node_type is Node.DELEGATE:
            delegated_node, = graph.successors(node)
            init_object(graph, delegated_node, context_vars, global_vars, type_cache)
            delegated_context, delegated_name = delegated_node
            obj = context_vars[delegated_context][delegated_name]
        else:
            initiator, = graph.inquirer.select(node, 'value')
            if initiator in type_cache:
                obj = type_cache[initiator]
            else:
                args = {}
                for m in graph.successors(node):
                    init_object(graph, m, context_vars, global_vars, type_cache)
                    child_context, child_name = m
                    args[child_name] = context_vars[child_context][child_name]
                
                obj = initiator(**args)
                type_cache[initiator] = obj
        
        context_vars[context][node_name] = obj
