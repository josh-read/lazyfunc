import inspect
import operator
from functools import cached_property
from mfunc.utils import insert


def has_dunder(name):
    return name.startswith('__') and name.endswith('__')


DUNDER_METHODS = [func_name for func_name, _ in inspect.getmembers(operator, inspect.isbuiltin) if has_dunder(func_name)]


class Operator:

    def __init__(self, name, precedence, has_reverse=None):
        self.name = name
        self.precedence = precedence
        self._has_reverse = has_reverse

    @cached_property
    def func(self):
        return getattr(operator, self.name)

    @property
    def number_of_operands(self):
        sig = inspect.signature(self.func)
        return len(sig.parameters)

    @property
    def has_reverse(self):
        if self._has_reverse is None:
            return self.number_of_operands == 2  # most dyadic operators have reverse variants
        else:
            return self._has_reverse

    @property
    def has_inplace_variant(self):
        inplace_name = insert(self.name, 'i', 2)
        return inplace_name in DUNDER_METHODS

    def format(self, instance, other=None):
        doc_template = (self.func.__doc__
                         .removeprefix('Same as ')
                         .removesuffix('.')
                         .removesuffix(', for a and b sequences')  # concat
                         .removesuffix(' (note reversed operands)'))  # contains
        doc_filled = doc_template.replace('a', instance)
        if other is not None:
            doc_filled = doc_filled.replace('b', other)
        return doc_filled


operators = [
    Operator('__pow__', precedence=15),
    Operator('__pos__', precedence=14),
    Operator('__neg__', precedence=14),
    Operator('__invert__', precedence=14),
    Operator('__mul__', precedence=13),
    Operator('__matmul__', precedence=13),
    Operator('__truediv__', precedence=13),
    Operator('__floordiv__', precedence=13),
    Operator('__mod__', precedence=13),
    Operator('__add__', precedence=12),
    Operator('__sub__', precedence=12),
]
