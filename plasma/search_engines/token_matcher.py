import difflib

from .index import Index
from ..data_model.collections import Stream


class TokenMatcher:

    def __init__(self, index:Index, threshold:float):
        super().__init__()

        self._index = index
        self.threshold = threshold
    
    def __call__(self, tokens:list[str]):
        return dict(
            Stream(tokens).product(self._index.tokens)
            .groupby(
                lambda qtk, _: qtk, 
                lambda qtk, rtk: (rtk, difflib.SequenceMatcher(None, qtk, rtk))
            ).select(lambda _, ms: {qtk: m.ratio() for qtk, m in ms})
        )
