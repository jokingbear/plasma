from rich.console import Console


def rich_repr(a):
    with Console(force_jupyter=False, force_terminal=True) as console:
        with console.capture() as capture:
            console.print(a)
        
        return capture.get()
