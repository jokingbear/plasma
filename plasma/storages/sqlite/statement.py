from collections.abc import Sequence
from sqlite3 import Connection

from ...functional import ReadableClass


class Statement(ReadableClass):
    
    def __init__(self, text:str, params:Sequence, execute_many:bool):
        super().__init__()
        
        self.text = text
        self.params = params
        self.many_strategy = execute_many
    
    def parameterize(self, *params, execute_many:bool=False):
        return Statement(self.text, params, execute_many)

    def execute(self, connection:Connection):
        if self.many_strategy:
            return connection.executemany(self.text, self.params)
        else:
            return connection.execute(self.text, self.params)

    def _tree(self, tree):
        statement = tree.add('statement')
        statement.add(self.text.strip())
        
        if len(self.params) > 0:
            params = tree.add('params')
            params.add(f'{self.params[:5]}')

        return tree
