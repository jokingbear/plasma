import inspect
import itertools

from typing import Any, Hashable, Iterable, Sequence, Callable

from .tuple_dict import TupleDict
from ....object_inquirer import ObjectInquirer
from .....base_model import Field
from ......functional import AutoPipe


class Projector[T]:
    
    def __init__(
            self, 
            inquirer:T,
            attributes:Sequence[str|Field],
            funcs:Sequence[tuple[str, Field|str|Callable[[Hashable, T, TupleDict], Any]]],
            default:object,
        ):
        super().__init__()
        
        self.inquirer = inquirer
        self.attributes = attributes
        self.funcs = funcs
        self.default = default
    
    def __call__(self, node_id:Hashable, obj_inquirer:ObjectInquirer):
        attribute_values = [obj_inquirer.get(a, self.default) for a in self.attributes]
        results = TupleDict([*self.attributes], attribute_values)
        
        for name, func in self.funcs:
            if func in results:
                qresult = results[func]
            elif isinstance(func, (str, Field)):
                qresult = obj_inquirer.get(func, self.default)
            else:
                qresult = func(node_id, self.inquirer, results)
            
            results.update(name, qresult)
        
        return results

    def __len__(self):
        return len(self.attributes) + len(self.funcs)

    def update(
            self, 
            attributes:Sequence[str|Field], 
            funcs:Iterable[tuple[str, str|Field|Callable[[Hashable, T, TupleDict], Any]]],
            default:object,
            override:bool,
        ):
        return Projector(
            self.inquirer,
            attributes if override else [*self.attributes, *attributes],
            tuple(funcs) if override else tuple(itertools.chain(self.funcs, funcs)),
            default=default
        )
