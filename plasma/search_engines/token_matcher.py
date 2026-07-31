import difflib

from .index import Index
from ..data_model.collections import Stream, ZippedStream


class TokenMatcher:

    def __init__(self, index:Index, threshold:float, topk:int|None):
        super().__init__()

        self._index = index
        self.threshold = threshold
        self.topk = topk
    
    def __call__(self, tokens:list[str]):
        return dict(
            Stream(tokens).product(self._index.tokens)
            .groupby(
                lambda qtk, _: qtk, 
                lambda qtk, rtk: (rtk, difflib.SequenceMatcher(None, qtk, rtk))
            )
            .map_value(lambda _, ms: 
                ZippedStream(ms)
                .select(lambda qtk, sm: (qtk, sm.ratio()))
                .filter(lambda _, s: s >= self.threshold)
                .sort(lambda _, s: s, reverse=True)
            )
            .select(lambda _, ms: {qtk: score for qtk, score in ms[:self.topk]})
        )
