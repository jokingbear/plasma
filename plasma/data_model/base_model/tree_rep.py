from rich.tree import Tree
from .utils import is_data_model
from ...utils import rich_repr


def tree_repr[T](cls:type[T]) -> type[T]:
    def _tree(self:T, tree:Tree):
        for a in cls.__annotations__:
            _render_tree(a, getattr(self, a), tree)

        return tree
    
    def __repr__(self:T):
        tree = Tree(type(self).__name__)
        return rich_repr(cls._tree(self, tree)) # type:ignore - python limit
    
    if not hasattr(cls, '_tree'):
        cls._tree = _tree # type:ignore
    
    cls.__repr__ = __repr__
    return cls


def _render_tree(field_name, obj, tree:Tree): 
    if is_data_model(obj):
        tree = tree.add(f'{field_name}={type(obj).__name__}')

        for a in type(obj).__annotations__:
            _render_tree(a, getattr(obj, a), tree)
    elif isinstance(obj, (tuple, list)):
        tree = tree.add(f'{field_name}={type(obj).__name__}')
        for i, o in enumerate(obj):
            _render_tree(str(i), o, tree)
    else:
        tree.add(f'{field_name}={obj}')
