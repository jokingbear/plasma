import inspect
import networkx as nx

from warnings import warn


class DependencyManager:

    def __init__(self, dep_graph:nx.DiGraph=None):
        super().__init__()
        
        self._dep_graph = dep_graph or nx.DiGraph()
    
    def add_dependency(self, name, value, as_singleton=False):
        assert as_singleton or callable(value), 'depdency should be callable'
        
        if name in self._dep_graph and self._dep_graph.out_degree(name) > 0:
            warn(f'{name} is already registered, overwriting it.')
            neighbors = [*self._dep_graph.neighbors(name)]
            self._dep_graph.remove_edges_from([(name, n) for n in neighbors])
        
        if as_singleton:
            self._dep_graph.add_node(name, value=value)    
        else:
            self._dep_graph.add_node(name, initiator=value)
            
            parameters = inspect.signature(value).parameters
            for arg_name, p in parameters.items():
                if arg_name != 'self':
                    attrs = {}
                    if p.annotation is not inspect._empty:
                        attrs['annotation'] = p.annotation

                    self._dep_graph.add_node(arg_name, **attrs)
                    self._dep_graph.add_edge(name, arg_name)
                    
                    if p.default is not inspect.Parameter.empty:
                        self._dep_graph.add_node(arg_name, value=p.default)

        return self

    def merge(self, manager, **collision_maps):
        assert isinstance(manager, DependencyManager), 'manager must be meta.object_graph.Manager instance'
        
        current_graph = self._dep_graph.copy()
        overwriter = manager._dep_graph.copy()
        
        if len(collision_maps) > 0:
            overwriter = nx.relabel_nodes(overwriter, collision_maps)

        collisions = set(current_graph).intersection(overwriter)
        if len(collisions) > 0:
            warn(f'name collision after merging at: {collisions}')

            for n in collisions:
                edges = [*current_graph.edges(n)]
                current_graph.remove_edges_from(edges)
        
        new_graph = nx.compose(current_graph, overwriter)
        return type(self)(new_graph)

    def duplicate(self, current_name:str, new_name:str, inplace=True):
        assert current_name in self._dep_graph, 'current name must be in dep graph'
        assert new_name not in self._dep_graph, 'new name must not be in dep graph'
        
        current_graph = self._dep_graph
        if not inplace:
            current_graph = current_graph.copy()
        
        node = current_graph.nodes[current_name]
        neighbors = [*current_graph.successors(current_name)]
        current_graph.add_node(new_name, **node)
        for n in neighbors:
            current_graph.add_edge(new_name, n)
        
        return type(self)(current_graph)
