from typing import Sequence

from .index import Index
from .regex_tokenizer import RegexTokenizer
from .inquirer import PathInquirer, QueryMatch, Match
from .token_matcher import TokenMatcher
from ..data_model.collections import (
    ZippedStream, GroupStream, Stream
)
from ..functional import ReadableClass
from ..utils import Formatter


class StreamIndex(ReadableClass):
    
    def __init__(
            self, 
            data:Sequence[str],
            group_splitter=r'[^\.\n]+', tokenizer=r'\w+',
            token_threshold=0.7
        ):
        super().__init__()
        
        tokenizer = RegexTokenizer(tokenizer)
        index = Index(data, tokenizer)
        token_matcher = TokenMatcher(index, token_threshold)
        
        self._index = index
        self.context_splitter = RegexTokenizer(group_splitter)
        self.path_inquirer = PathInquirer(self._index, tokenizer, token_matcher)
    
    def __call__(self, query:str):
        contexts = self.context_splitter(query)
        return QueryResults(
            query,
            ZippedStream[int, int, str](contexts.itertuples(index=False))
            .unwind(lambda start, end, context:
                self.path_inquirer(context)
                .select(lambda m:m.update(start))
            ).groupby(lambda m: m.query, lambda m: m)
        )

    def run(self, query:str):
        return self(query)


class QueryResults(ReadableClass):
    
    def __init__(self, 
            query:str,
            group_results:GroupStream[QueryMatch, Match]
        ):
        super().__init__()

        self.query = query
        self._stream = (
            group_results.select(lambda qm, ms:
                Stream(ms)
            )
        )
    
    def _tree(self, tree):
        query = self.query
        tree.add(f'query={query}')
        
        match_repr = tree.add('matches')
        for qmatch, matches in self._stream.take(10):
            rep = Formatter.BOLD(
                f'{qmatch.start} - {qmatch.end}: {qmatch.slice(query)}'
            )
            qtree = match_repr.add(rep)
            for m in matches.take(5):
                qtree.add(f'{m.db.arg} - {m.db.slice()} - {m.db.value}')

        return tree
