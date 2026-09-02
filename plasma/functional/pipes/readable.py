from rich.tree import Tree

from ...utils import rich_repr


class ReadableClass:
    
    def __init__(self):
        self._marked_attributes = []
    
    def mark(self, attr:str):
        assert hasattr(self, attr), f'{type(self)} does not have attribute {attr}'
        self._marked_attributes.append(attr)
        return self
    
    def _root_repr(self):
        return type(self).__name__
    
    def _tree(self, tree:Tree):
        for a in self._marked_attributes:
            val = getattr(self, a)
            
            if isinstance(val, ReadableClass):
                val._tree(tree.add(f'{a}={val._root_repr()}'))
            else:
                child = f'{a}={repr(val).strip()}'
                tree.add(child)
        
        return tree
    
    def _full_tree(self):
        root = Tree(self._root_repr())
        return self._tree(root)

    def __setattr__(self, key:str, value):
        if key[0] != '_' and key not in self._marked_attributes:
            self._marked_attributes.append(key)

        super().__setattr__(key, value)

    def __repr__(self):
        return rich_repr(self._full_tree())
