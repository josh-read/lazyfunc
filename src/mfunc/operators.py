import inspect
import operator
from functools import cached_property


def has_dunder(name):
    return name.startswith('__') and name.endswith('__')


DUNDER_METHODS = [func_name for func_name, _ in inspect.getmembers(operator, inspect.isbuiltin) if has_dunder(func_name)]


class Operator:

    def __init__(self, name, precedence=0):
        self.name = name
        self.precedence = precedence

    @cached_property
    def func(self):
        return getattr(operator, self.name)

    @cached_property
    def number_of_operands(self):
        sig = inspect.signature(self.func)
        return len(sig.parameters)

    @cached_property
    def operation_format_template(self):
        operation_doc = (self.func.__doc__
                         .removeprefix('Same as ')
                         .removesuffix('.')
                         .removesuffix(', for a and b sequences')  # concat
                         .removesuffix(' (note reversed operands)'))  # contains
        return operation_doc.replace('a', '{}').replace('b', '{}').replace('c', '{}')


operators = [
        Operator('__pow__', precedence=15),
        Operator('__mul__', precedence=13),
        Operator('__truediv__', precedence=13),
        Operator('__add__', precedence=12),
        Operator('__sub__', precedence=12),
    ]
