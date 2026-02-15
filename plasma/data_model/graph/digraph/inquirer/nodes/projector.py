import inspect
import itertools

from typing import Hashable, Iterable

from .tuple_dict import TupleDict
from ....object_inquirer import ObjectInquirer
from .....base_model import Field
from ......functional import AutoPipe


class SelectFunc[T](AutoPipe[[Hashable, T], object]):...
class SelectFuncAggregate[T](AutoPipe[[Hashable, T, TupleDict], object]):...


class Projector[T](AutoPipe[[Hashable, ObjectInquirer], TupleDict]):
    
    def __init__(self, 
                inquirer:T,
                attributes:tuple[str|Field],
                funcs:tuple[tuple[str, SelectFunc[T]|SelectFuncAggregate[T]]],
                default:object,
            ):
        self.inquirer = inquirer
        self.attributes = attributes
        self.funcs = funcs
        self.default = default
    
    def run(self, node_id:Hashable, obj_inquirer:ObjectInquirer):
        attribute_values = [obj_inquirer.get(a, self.default) for a in self.attributes]
        results = TupleDict([*self.attributes], attribute_values)
        
        for name, f in self.funcs:
            if isinstance(f, str):
                if f in results:
                    results.rename(f, name)
                else:
                    results.update(name, obj_inquirer.get(f, self.default))
            else:
                signature = inspect.signature(f)
                if len(signature) == 2:
                    results.update(name, f(node_id, self.inquirer))
                elif len(signature) == 3:
                    results.update(name, f(node_id, self.inquirer, results))
        
        return results

    def __len__(self):
        return len(self.attributes) + len(self.funcs)

    def update(self, 
               attributes:tuple[str|Field], 
               funcs:Iterable[tuple[str, SelectFunc[T]|SelectFuncAggregate[T]]],
               default:object,
               override:bool,
            ):
        return Projector(
            self.inquirer,
            attributes if override else {*self._projector.attributes, *attributes},
            tuple(funcs) if override else tuple(itertools.chain(self.funcs, funcs)),
            default=default
        )
