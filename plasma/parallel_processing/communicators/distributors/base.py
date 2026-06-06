from ...queues import Queue


class Distributor[T]:

    def run(self, data:T, *queues:Queue, **named_queues:Queue):...
    
    def __call__(self, data:T, *queues:Queue, **named_queues:Queue):
        return self.run(data, *queues, **named_queues)
    
    def __repr__(self):
        return f'{type(self)}'
