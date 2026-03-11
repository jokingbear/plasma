import networkx as nx


class SchemaGraph(nx.DiGraph):
    root:object
    
    def type(self, node) -> tuple[type, tuple[type]]:...


class Repr:
    
    def __init__(self, graph:SchemaGraph):
        self.lines = list[str]()
        self.graph = graph

    def run(self):
        self._iterate(self.graph.root)
        lines = self.lines
        lines[0] = lines[0].replace('|->:', '')

        return '\n'.join(lines)

    def _iterate(self, node, indent=''):
        origin, args = self.graph.type(node)
        
        type_str = origin.__name__
        if len(args) > 0:
            type_str += f'[{','.join(a.__name__ for a in args)}]'
        key = '' if len(node) == 0 else node[-1]     
        self.lines.append(f'{indent}|->{key}:{type_str}')

        for s in self.graph.successors(node):
            self._iterate(s, indent=indent + ' ' * 2)
