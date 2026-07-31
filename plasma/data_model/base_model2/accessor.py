class Accessor:
    
    def __init__(self, *args:str):
        self.components = args
    
    def prepend(self, *parents:str):
        return Accessor(*parents, *self.components)
    
    def __repr__(self):
        return '.'.join(self.components)

    def __len__(self):
        return len(self.components)
    
    def __contains__(self, other:"Accessor"):
        return other.components == self.components[:len(other.components)]
