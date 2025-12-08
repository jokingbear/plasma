from .chainable_graph import ChainableGraph
from dataclasses import dataclass
from ...queues import Queue
from ..distributors import UniformDistributor, Distributor


class AdaptableGraph(ChainableGraph):
    
    def chain(self, *chains:tuple[Queue, object]|tuple[object, Queue]|tuple[object, object]\
                            |tuple[object, Queue, object]|tuple[object, object, Queue]|tuple[Queue, object, Distributor]\
                            |tuple[object, Queue, object, Distributor]|tuple[object, object, Queue, Distributor]):
        standardized_chains = [_standardize_inputs(b).to_tuple() for b in chains]
        return super().chain(*standardized_chains)


@dataclass
class Link:
    head:object
    connector:Queue
    tail:object
    distributor:Distributor = UniformDistributor()
    
    def to_tuple(self):
        return self.head, self.connector, self.tail, self.distributor


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
        elif isinstance(block[0], Queue):
            block = Link(None, *block)
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
