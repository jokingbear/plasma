from tqdm.auto import tqdm


class Tracker[T]:
    
    def __init__(self, **tqdm_args):
        self._progress_bar = tqdm(**tqdm_args)

    def __call__(self, x:T):
        self._progress_bar.update()
        return x
