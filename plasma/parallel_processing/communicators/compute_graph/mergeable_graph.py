import networkx as nx

from .readable_graph import ReadableGraph
from ...queues import Queue
from ..distributors import Distributor


class MergeableGraph(ReadableGraph):
    
    def chain(self, *chains):
        validate_chains(chains)
        
        simple_chains, complex_chains = filter_chains(chains)
        for c in complex_chains:
            block, graph = c
            graph: MergeableGraph
            self._structures = nx.compose(self._structures, graph._structures)
            simple_chains.append((block, graph.input))
        
        return super().chain(*simple_chains)


def validate_chains(chains:list[tuple]):
    try:
        for c in chains:
            validate_single(c)
    except AssertionError as e:
        raise SyntaxError('incorrect syntax') from e


def validate_single(chain:tuple):
    if len(chain) == 2:
        node1, node2 = chain
        assert not isinstance(node1, (Queue, MergeableGraph)) or not isinstance(node2, (Queue, MergeableGraph)), \
            f'Queue/Graph -> Queue/Graph is ambiguous, currently {type(node1)} -> {type(node2)}'
    else:
        for b in chain:
            assert not isinstance(b, MergeableGraph), 'Mergeable Graph in 3-4 tuple is ambiguous'


def filter_chains(chains:list[tuple]):
    simple_chains = []
    complex_chains = []
    for c in chains:
        if len(c) == 2 and isinstance(c[-1], MergeableGraph):
            complex_chains.append(c)
        else:
            simple_chains.append(c)
    
    return simple_chains, complex_chains
