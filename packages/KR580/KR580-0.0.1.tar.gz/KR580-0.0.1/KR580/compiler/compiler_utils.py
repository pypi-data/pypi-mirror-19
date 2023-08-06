from multipledispatch import dispatch

from .opcodes import Opcode

@dispatch(list, int)
def construct_list(a, b):
    return a + [b]

@dispatch(int, list)
def construct_list(a, b):
    return [a] + b

@dispatch(int, int)
def construct_list(a, b):
    return [a, b]

@dispatch(list, list)
def construct_list(a, b):
    return a + b

def resolve_name(p):
    return getattr(Opcode, '_'.join(p[1:])).value
