from rich.tree import Tree
from rich.markup import escape
from typing import get_origin

from ..arch import ITEM_PREFIX, SCHEMA_FIELD
from ..accessor import Accessor
from .....functional import ReadableClass


class Repr(ReadableClass):
    root:Accessor
    
    def _root_repr(self):
        return repr(self.root)
    
    def _tree(self, tree):
        children = Accessor.get_children(self.root)
        for a in children:
            tree.add(_render(a))

        return tree


def _render(a:Accessor):
    children = [*Accessor.get_children(a)]
    name = Accessor.get_name(a)
    t = Accessor.get_value(a)
    t_repr = _render_type(Accessor.get_value(a))

    tree = Tree(f'{name}: {t_repr}')
    if len(children) == 1 and ITEM_PREFIX in Accessor.get_name(children[0]):
        t_repr = _render_type(get_origin(t)) #type:ignore
        tree = Tree(f'{name}: {t_repr}')
        tree.add(_render(children[0]))
        return tree
    elif len(children) > 0:
        rep_inst:Repr = getattr(t, SCHEMA_FIELD)
        return rep_inst._tree(tree)
        
    return tree


def _render_type(t:type):
    t_repr = repr(t)
    if 'class' in t_repr:
        return t.__name__
    
    return escape(repr(t))
