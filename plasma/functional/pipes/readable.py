from rich.tree import Tree

from ...utils import rich_repr


class ReadableClass:
    
    def __init__(self):
        self._marked_attributes = []
    
    def mark(self, attr:str):
        assert hasattr(self, attr), f'{type(self)} does not have attribute {attr}'
        self._marked_attributes.append(attr)
        return self
    
    def _tree(self):
        tree = Tree(type(self).__name__)
        
        for a in self._marked_attributes:
            val = getattr(self, a)
            
            if isinstance(val, ReadableClass):
                child = val._tree()
            else:
                child = repr(val)
            
            tree.add(child)
        
        return tree

    def __setattr__(self, key:str, value):
        if key[0] != '_' and key not in self._marked_attributes:
            self._marked_attributes.append(key)

        super().__setattr__(key, value)

    def __repr__(self):
        return rich_repr(self._tree())
