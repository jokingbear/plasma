import re

from collections.abc import Sequence
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Any

from ..protocols import SqlStatement
from ...functional import ReadableClass


@dataclass
class SqliteStatement(SqlStatement[Connection], ReadableClass):
    text:str
    args:Sequence | dict[str, Any]
    execute_many:bool = False
    
    @property
    def dml(self):
        return re.search('INSERT|UPDATE|CREATE', self.text) is not None

    def parameterize(self, *args, execute_many:bool|None = None, **kwargs):
        assert len(args) == 0 or len(kwargs) == 0, 'cant have both args and kwargs'

        if len(args) == 0 and len(kwargs) == 0:
            args = self.args
        elif len(args) == 0:
            args = kwargs
            
        execute_many = self.execute_many if execute_many is None else execute_many
        return SqliteStatement(
            self.text, args, execute_many
        )

    def execute(self, connector: Connection):
        if self.execute_many:
            return [*connector.executemany(self.text, self.args)]
        
        return connector.execute(self.text, self.args)

    def _tree(self, tree):
        tree.add(f'statement\n{self.text.strip()}')
        
        if len(self.args) > 0:
            params = tree.add('args')
            params.add(f'{self.args}')

        return tree
