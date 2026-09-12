import pickle

from .protocols import Serializer


class Pickler(Serializer):

    def serialize(self, x):
        return pickle.dumps(x)

    def deserialize(self, x):
        return pickle.loads(x)
