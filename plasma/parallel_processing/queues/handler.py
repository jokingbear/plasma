from warnings import deprecated


@deprecated('use function with the same signature')
class ExceptionHandler:
    
    def __call__(self, data, e:Exception):
        raise e
