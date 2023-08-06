import contextlib

_state = {
    "matrix": "709"
}


def set_state(name, value):
    _state[name] = value

def get_state(name):
    return _state[name]

@contextlib.contextmanager
def state(name, value):
    old = get_state(name)
    try:
        set_state(name, value)
        yield
    finally:
        set_state(name, old)
