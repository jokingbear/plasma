from rich.tree import Tree
from rich.console import Console
from typing import Sequence

from .inquirer import is_data_model


class Repr:
    
    def __call__(self, obj):
        root = Tree('')
        self._render_tree('', obj, root)
        
        with Console(force_terminal=True, force_jupyter=False) as console:
            with console.capture() as capture:
                console.print(root.children[0])
            return capture.get()[1:]
    
    def _render_tree(self, field_name, obj, tree:Tree): #type:ignore        
        if is_data_model(obj):
            tree = tree.add(f'{field_name}={type(obj).__name__}')

            for a in obj.__annotations__:
                self._render_tree(a, getattr(obj, a), tree)
        elif isinstance(obj, (tuple, list)):
            tree = tree.add(f'{field_name}={type(obj).__name__}')
            for i, o in enumerate(obj):
                self._render_tree(str(i), o, tree)
        else:
            tree.add(f'{field_name}={obj}')
