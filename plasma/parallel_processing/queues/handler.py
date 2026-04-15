import plasma.functional as F


class ExceptionHandler:
    
    def __call__(self, data, e:Exception):
        raise e
