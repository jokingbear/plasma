from ...queues import Queue


class Distributor[T]:

    def run(self, data:T, *queues:Queue, **named_queues:Queue):...
    
    def __repr__(self):
        return f'{type(self)}'
