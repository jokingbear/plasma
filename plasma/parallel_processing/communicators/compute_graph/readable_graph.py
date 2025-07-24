import networkx as nx

from .adaptable_graph import AdaptableGraph
from ...queues import Queue
from ..distributors import UniformDistributor
from ....functional import proxy_func


class ReadableGraph(AdaptableGraph):

    @property
    def input(self) -> Queue:
        structures = self._structures
        node_types = nx.get_node_attributes(structures, 'object')
        for n, t in node_types.items():
            if isinstance(t, Queue) and structures.in_degree(n) == 0:
                return t
        
        raise LookupError('the graph does not have an input')
    
    def __repr__(self):     
        lines = []
        self._render_lines(id(self.input), set(), '', lines)
        
        return '\n\n'.join(lines)
    
    def _render_lines(self, key, rendered:set, prefix='', lines=[]):
        structures = self._structures
        node_attributes = structures.nodes[key]
        if isinstance(node_attributes['object'], Queue):
            queue:Queue = node_attributes['object']
            line = f'[{type(queue).__name__}(name={queue.name}, runner={queue.num_runner})]'
        else:
            obj = node_attributes['object']
            
            if 'function' in type(obj).__name__ or isinstance(obj, proxy_func):
                name = f'{obj}'
            else:
                name = type(obj).__name__
            line = f'({name}, id={key})'
            distributor = node_attributes['distributor']
            if not isinstance(distributor, UniformDistributor):
                line = f'{line}-{type(distributor).__name__}'
            
            if key in rendered:
                line = line + '...'
            rendered.add(key)
            
        if structures.in_degree(key) > 0:
            line = '|->' + line
            
        line = prefix + line
        lines.append(line)      
        if '...' != line[-3:]:
            for n in structures.successors(key):
                self._render_lines(n, rendered, prefix + ' ' * 2, lines)
