import networkx as nx

from ...functional import State, partials, proxy_func, Identity, decorators
from ..queues import Queue
from .distributors import Distributor, UniformDistributor
from ._proxy import ProxyIO
from dataclasses import dataclass
from enum import Enum


class ComputeGraph[T]:

    def __init__(self):
        self._structures = nx.DiGraph()

    def chain(self, *blocks:tuple[Queue, T]|tuple[T, T]|tuple[T, Queue]\
                            |tuple[T, T, Queue]|tuple[T, Queue, T]\
                            |tuple[T, T, Queue, Distributor]|tuple[T, Queue, T, Distributor]):
        for block in blocks:      
            link = _standardize_inputs(block)          
            
            assert not isinstance(link.head, Queue)
            assert not isinstance(link.tail, Queue)
            
            self._add_block(link.head)
            self._add_block(link.tail, link.distributor)
            self._add_queue(link.connector)
            
            if link.head is None:
                self._structures.add_edge(id(link.connector), id(link.tail))
            elif link.tail is None:
                self._structures.add_edge(id(link.head), id(link.connector))
            elif link.connector is None:
                connector = [*self._structures.predecessors(id(link.tail))]
                assert len(connector) == 1
                connector = connector[0]
                self._structures.add_edges_from([(id(link.head), connector), 
                                                 (connector, id(link.tail))])
            else:
                self._structures.add_edges_from([(id(link.head), id(link.connector)), 
                                                 (id(link.connector), id(link.tail))])
        
        return self

    @decorators.propagate(None)
    def _add_queue(self, queue):
        self._structures.add_node(id(queue), object=queue, type=NodeType.Queue)
    
    @decorators.propagate(None)
    def _add_block(self, block, distributor=None):
        self._structures.add_node(id(block), object=block, type=NodeType.Block, 
                                distributor=distributor or UniformDistributor())

    @property
    def input(self) -> Queue:
        structures = self._structures
        node_types = nx.get_node_attributes(structures, 'type')
        for n, t in node_types.items():
            if t is NodeType.Queue and structures.in_degree(n) == 0:
                return structures.nodes[n]['object']
        
        raise LookupError('the graph does not have an input')
    
    def __repr__(self):     
        lines = []
        self._render_lines(id(self.input), set(), '', lines)
        
        return '\n'.join(lines)
    
    def _render_lines(self, key, rendered:set, prefix='', lines=[]):
        structures = self._structures
        node_attributes = structures.nodes[key]
        if node_attributes['type'] is NodeType.Queue:
            queue:Queue = node_attributes['object']
            line = f'[{type(queue).__name__}(name={queue.name}, runner={queue.num_runner})]'

        else:
            obj = node_attributes['object']
            
            if 'function' in type(obj).__name__ or isinstance(obj, proxy_func):
                name = f'{obj}'
            else:
                name = type(obj).__name__
            
            distributor = node_attributes['distributor']
            line = f'({name})-{type(distributor).__name__}'
        
        if structures.in_degree(key) > 0:
            line = '|->' + line
            
        line = prefix + line
        lines.append(line)
        for n in structures.successors(key):
            self._render_lines(n, rendered, prefix + ' ' * 2, lines)


@dataclass
class Link:
    head:str
    connector:Queue
    tail:str
    distributor:Distributor = None


def _standardize_inputs(block:tuple) -> Link:
    if len(block) == 2:
        if isinstance(block[0], Queue):
            block = Link(None, *block)
        elif  isinstance(block[1], Queue):
            block = Link(*block, None)
        else:
            block = Link(block[0], None, block[1])
    elif len(block) == 3:
        none_counts = len([a for a in block if a is None])
        assert none_counts < 2, f'{block} has more than one None'
        
        block = [a for a in block if a is not None]
        if len(block) == 2:
            block = _standardize_inputs(block)
        else:
            link1 = _standardize_inputs(block[:2])
            link2 = _standardize_inputs(block[1:])
            block = Link(link1.head or link2.head, 
                         link1.connector or link2.connector, 
                         link1.tail or link2.tail)
    elif len(block) == 4:
        distributor = block[-1]
        assert distributor is not None
        link = _standardize_inputs(block[:-1])
        block = Link(link.head, link.connector, link.tail, distributor)
    else:
        raise RuntimeError(f'unsupported type')
    
    return block


class NodeType(Enum):
    Block = 0
    Queue = 1
