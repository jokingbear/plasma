from .graph import Graph
from dataclasses import dataclass
from ...queues import Queue
from ..distributors import UniformDistributor, Distributor


class AdaptableGraph[T](Graph[T]):
    
    def chain(self, *blocks):
        standardized_blocks = [_standardize_inputs(b).to_tuple() for b in blocks]
        return super().chain(*standardized_blocks)


@dataclass
class Link:
    head:str
    connector:Queue
    tail:str
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
