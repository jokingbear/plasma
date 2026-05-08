from .operators import Operator


class Chain[I, O]:...


class Chain[I, O]:
    
    def __init__[T](self, chain:Chain[I, T], op:Operator[T, O]):
        self.prevs = chain
        self.op = op

    def next[V](self, op:Operator[O, V]):
        return Chain[I, V](self, op)
