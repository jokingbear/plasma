import networkx as nx


class Repr:
    
    def __init__(self, realization:nx.DiGraph):
        self.lines = []
        self.graph = realization
    
    def run(self):
        self._iterate(self.graph.root)
        lines = self.lines
        lines[0] = lines[0].replace('|-> = ', '')

        return '\n'.join(lines)
    
    def _iterate(self, node, indent=''):
        if len(node) == 0:
            key = ''
        else:
            key = str(node[-1])
        value = self.graph.nodes[node]['value']              
        self.lines.append(f'{indent}|->{key} = {type(value).__name__}')

        for s in self.graph.successors(node):
            self._iterate(s, indent=indent + ' ' * 2)
