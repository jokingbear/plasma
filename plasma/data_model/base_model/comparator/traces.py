from scipy.stats import hmean
from typing import Any, Sequence, Self
from rich.tree import Tree
from ..base2 import model
from ....utils import rich_repr


@model
class StandardTrace:
    target:Any
    ref:Any
    score:float


@model
class SummaryTrace:
    score:float
    items:Sequence[StandardTrace|Self]


class Summary:
    
    def __init__(self, num_target, num_refs, traces:dict[str, StandardTrace|SummaryTrace]):
        precisions = [max(t.score, 0.1) for t in traces.values()]
        precisions.extend([0.1] * (num_target - len(traces)))

        precision = hmean(precisions)
        recall = sum([max(t.score, 0.1) for t in traces.values()], 0) / num_refs
        score = hmean([precision, recall])
        
        self.precision = precision
        self.recall = recall
        self.score = score
        self.traces = traces
    
    def __repr__(self):
        tree = Tree(type(self).__name__)
        
        tree.add(f'score={self.score:.04f}')
        tree.add(f'precision={self.precision:.04f}')
        tree.add(f'recall={self.recall}')
        
        for k, v in self.traces.items():
            tree.add(f'{k}={v.score:.04f}')
        
        return rich_repr(tree)
