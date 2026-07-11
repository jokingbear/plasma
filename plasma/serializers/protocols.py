from typing import Protocol


class Serializer(Protocol):

    def serialize(self, x) -> bytes:...
    
    def deserialize(self, x:bytes):...
