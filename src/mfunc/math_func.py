import operator
import numbers

from mfunc.utils import callable_name, add_parentheses


def new_func_from_operation(self, other, operation):
    if callable(other):
        return lambda *x: operation(self(*x), other(*x))
    elif isinstance(other, numbers.Real):
        return lambda *x: operation(self(*x), other)
    else:
        msg = f"Cannot call {operation.__name__} on MathFunc and type {type(other)}. " \
              f"Must be either callable or a scalar value."
        raise TypeError(msg)


def new_description_from_operation(self, other, operation_symbol, rank):
    self_desc = self.description
    if isinstance(other, MathFunc):
        other_desc = other.description
    elif callable(other):
        other_desc = callable_name(other)
    else:
        other_desc = str(other)

    self_rank = getattr(self, 'rank', None)
    if self_rank is None:
        pass
    elif self_rank < rank:
        self_desc = add_parentheses(self_desc)

    other_rank = getattr(other, 'rank', None)
    if other_rank is None:
        pass
    elif other_rank < rank:
        other_desc = add_parentheses(other_desc)

    return ' '.join((self_desc, operation_symbol, other_desc))


def math_operation(operation_name, operation, operation_symbol, rank):
    def inner(self, other):
        new_func = new_func_from_operation(self, other, operation)
        new_desc = new_description_from_operation(self, other, operation_symbol, rank)
        return MathFunc(func=new_func, description=new_desc, rank=rank)
    inner.__name__ = operation_name
    inner.__doc__ = f'Return new MathFunc with unevaluated function resulting from self {operation_symbol} other, ' \
                    f'where other may be a scalar value or any other callable including another MathFunc instance.'
    return inner


class MathFunc:

    __add__ = math_operation('__add__', operator.add, '+', 1)
    __mul__ = math_operation('__mul__', operator.mul, '*', 2)
    __truediv__ = math_operation('__truediv__', operator.truediv, '/', 2)

    def __init__(self, func, *args, description=None, rank=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description
        self.rank = rank

    @property
    def description(self):
        if self._description is None:
            return callable_name(self.func)
        else:
            return self._description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

    def __call__(self, *x):
        return self.func(*x, *self.args, **self.kwargs)


def math_func(func):
    return MathFunc(func)
