class Meta:
    
    def __init__(self):
        self._contexts:dict[str, set] = {}
    
    def init(self, context):
        if context not in self:
            self._contexts[context] = set()
    
    def add_name(self, context:str, name:str):
        self._contexts[context].add(name)
    
    def __iter__(self):
        yield from self._contexts
    
    def __getitem__(self, context:str):
        return self._contexts[context]
    
    def __contains__(self, other:str):
        return other in self._contexts
    
    def __repr__(self):
        lines = []
        lines.extend(f'{context}: {', '.join(names)}' 
                     for context, names in self._contexts.items())
        return '\n'.join(lines)
