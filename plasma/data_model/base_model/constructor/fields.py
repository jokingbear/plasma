from ..field import Field


class ParsedFieldDict(dict[str, object]):
    
    def __init__(self, field_values:dict[Field, object]):
        super().__init__()
        

def _resolve(fields_values:dict[Field, object], field:Field, results:dict):
    _, *accessors, name = field.context
    temp_dict = results
    for a in accessors:
        if a not in temp_dict:
            temp_dict[a] = {}
        temp_dict = temp_dict[a]
    
    temp_dict[name] = fields_values[field]