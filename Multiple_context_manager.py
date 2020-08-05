import contextlib

@contextlib.contextmanager
def propagator(name, propagate):
    try:
        yield
        print(name, 'exited normally')
    except Exception:
        print(name, 'received an exception!')
        if propagate:
            raise



with propagator('outer', True), propagator('inner', False):
    raise TypeError()
