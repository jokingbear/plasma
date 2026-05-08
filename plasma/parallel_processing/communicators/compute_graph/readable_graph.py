import networkx as nx

from rich.console import Console
from rich.tree import Tree

from .adaptable_graph import AdaptableGraph
from ..distributors import UniformDistributor
from ...queues import Queue
from ....functional import AutoPipe, Signature


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
        tree = Tree('')
        self._render_lines(id(self.input), tree, set())
        
        with Console(force_jupyter=False, width=140) as console:
            with console.capture() as capture:
                console.print(tree.children[0])
            return capture.get()
    
    def _render_lines(self, key, tree:Tree, rendered:set):
        structures = self._structures
        node_attributes = structures.nodes[key]
        if isinstance(node_attributes['object'], Queue):
            queue:Queue = node_attributes['object']
            line = f'[{type(queue).__name__}(name={queue.name}, runner={queue.num_runner}, id={key})]'
            line = f'[#6c6c6c]{line}[/#6c6c6c]'
        else:
            obj = node_attributes['object']
            
            if isinstance(obj, AutoPipe):
                signature = obj.signature()
            else:
                signature = Signature.from_func(obj)

            line = f'{signature.name}([({signature.inputs}) -> {signature.outputs}], id={key})'
            distributor = node_attributes['distributor']
            if not isinstance(distributor, UniformDistributor):
                line = f'{line}-{type(distributor).__name__}'
            
            if key in rendered:
                line = line + '...'
            
            line = f'[dodger_blue1]{line}[/dodger_blue1]'
            rendered.add(key)
            
        tree = tree.add(line)
        if '...' != line[-3:]:
            for n in structures.successors(key):
                self._render_lines(n, tree, rendered)

    @property
    def graph(self):
        return self._structures
    
    @property
    def queues(self):
        objects = nx.get_node_attributes(self._structures, 'object')
        for o in objects.values():
            if isinstance(o, Queue):
                yield o

    @property
    def internal_queues(self):
        for oid, attrs in self._structures.nodes.items():
            o = attrs['object']
            if isinstance(o, Queue) and self._structures.out_degree(oid) > 0:
                yield o

    def chain(self, *chains):
        try:
            return super().chain(*chains)
        except SyntaxError as e:
            print(self)
            raise e
