from dataclasses import dataclass
from scipy.stats import hmean
from typing import Any, Sequence, Self
from rich.tree import Tree
from ....utils import rich_repr, Formatter


@dataclass(repr=False)
class StandardTrace:
    target:Any
    ref:Any
    score:float
    
    def __repr__(self):
        tree = Tree(type(self).__name__)
        tree.add(Formatter.BLUE(f'target={self.target}'))
        tree.add(Formatter.GREEN(f'ref={self.ref}'))
        tree.add(f'score={self.score:.04f}')
        
        return rich_repr(tree)


@dataclass(repr=False)
class SummaryTrace:
    score:float
    items:Sequence[StandardTrace|Self]
    
    def __repr__(self):
        tree = Tree(type(self).__name__)
        tree.add(f'score={self.score:.04f}')
        
        items = tree.add('items')
        for i in self.items:
            items.add(repr(i).strip())
        
        return rich_repr(tree)


class Summary:
    
    def __init__(self, num_target, num_refs, traces:dict[str, StandardTrace|SummaryTrace]):
        precisions = [max(t.score, 0.1) for t in traces.values()]
        precisions.extend([0.1] * (num_target - len(traces)))

        precision = hmean(precisions)
        recall = sum([t.score for t in traces.values()], 0) / num_refs
        score = hmean([precision, recall])
        
        self.precision = precision
        self.recall = recall
        self.score = score
        self.traces = traces
    
    def __repr__(self):
        tree = Tree(type(self).__name__)
        
        tree.add(f'score={self.score:.04f}')
        tree.add(f'precision={self.precision:.04f}')
        tree.add(f'recall={self.recall:.04f}')
        
        traces = tree.add('traces')
        for k, v in sorted(self.traces.items(), key=lambda kv:kv[0]):
            metric = f'{k}={v.score:.04f}'
            if v.score < 0.5:
                metric = Formatter.RED(metric)
            elif v.score < 0.9:
                metric = Formatter.YELLOW(metric)

            traces.add(metric)
        
        return rich_repr(tree)
