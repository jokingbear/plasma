from typing import Protocol, Any


class Serializer(Protocol):

    def serialize(self, x) -> bytes:...
    
    def deserialize(self, x:bytes) -> Any:...
