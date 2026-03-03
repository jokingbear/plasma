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
        super().__init__()
        
        self.inquirer = inquirer
        self.attributes = attributes
        self.funcs = funcs
        self.default = default
    
    def run(self, node_id:Hashable, obj_inquirer:ObjectInquirer):
        attribute_values = [obj_inquirer.get(a, self.default) for a in self.attributes]
        results = TupleDict([*self.attributes], attribute_values)
        
        for name, f in self.funcs:
            if callable(f):
                signature = inspect.signature(f)
                has_args = any(p.kind is inspect._ParameterKind.VAR_POSITIONAL 
                               for p in signature.parameters.values())
                parameters = {k:p for k, p in signature.parameters.items() if k != 'self'}
                if has_args or len(parameters) > 2:
                    qresult = f(node_id, self.inquirer, results)
                elif len(parameters) == 2:
                    qresult = f(node_id, self.inquirer)
                else:
                    raise SyntaxError('unsupported signature, signature must be nodeid, inquirer or nodeid, inquirer, qdata')
            elif f in results:
                qresult = results[f]
            else:
                qresult = obj_inquirer.get(f, self.default)
            
            results.update(name, qresult)
        
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
            attributes if override else [*self.attributes, *attributes],
            tuple(funcs) if override else tuple(itertools.chain(self.funcs, funcs)),
            default=default
        )
