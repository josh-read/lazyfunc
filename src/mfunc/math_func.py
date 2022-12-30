import operator
import numbers
from warnings import warn

from mfunc.utils import callable_name, add_parentheses


def new_func_from_operation(self, other, operation):
    """Returns a function by combining self and other through a specified operation.
    Self must be of type MathFunc, other may be a scalar value or any callable including MathFunc"""
    if callable(other):
        return lambda *x: operation(self(*x), other(*x))
    elif isinstance(other, numbers.Real):
        return lambda *x: operation(self(*x), other)
    else:
        msg = f"Cannot call {operation.__name__} on MathFunc and type {type(other)}. " \
              f"Must be either callable or a scalar value."
        raise TypeError(msg)


def new_description_from_operation(self, other, operation_symbol, rank, reverse):
    """Returns a string describing the function resulting from combining self and other through
    the specified operation. The rank of the operation is compared to the rank of the last operation
    on self and other to determine whether parentheses are required."""
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

    other_rank = getattr(other, 'rank', None)  # if other is not a MathFunc, it will not have a rank attribute
    if other_rank is None:
        pass
    elif other_rank < rank:
        other_desc = add_parentheses(other_desc)

    if reverse:
        return ' '.join((other_desc, operation_symbol, self_desc))
    else:
        return ' '.join((self_desc, operation_symbol, other_desc))


def math_operation(operation_name, operation, operation_symbol, rank, reverse=False):
    """Function generator which produces the functions for arithmetic operations which are bound
    to MathFunc."""
    def inner(self, other):
        new_func = new_func_from_operation(self, other, operation)
        new_desc = new_description_from_operation(self, other, operation_symbol, rank, reverse)
        return MathFunc(func=new_func, description=new_desc, rank=rank)
    inner.__name__ = operation_name
    inner.__doc__ = f"Return new MathFunc with unevaluated function resulting from {'other' if reverse else 'self'} " \
                    f"{operation_symbol} {'self' if reverse else 'other'}, " \
                    "where other may be a scalar value or any other callable including another MathFunc instance."
    return inner


class MathFunc:
    """Wrap a callable object enabling arithmetic operations between it and scalar values or any other callables,
    including MathFunc instances."""

    __add__ = math_operation('__add__', operator.add, '+', 1)
    __radd__ = math_operation('__add__', operator.add, '+', 1, reverse=True)
    __sub__ = math_operation('__sub__', operator.sub, '-', 1)
    __mul__ = math_operation('__mul__', operator.mul, '*', 2)
    __truediv__ = math_operation('__truediv__', operator.truediv, '/', 2)
    __pow__ = math_operation('__pow__', operator.pow, '**', 3)

    def __init__(self, func, *args, description=None, rank=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description
        self.rank = rank

    @property
    def description(self):
        """Description of the function wrapped by the MathFunc. This information is presented in the
        __repr__. This defaults to the __name__ of the wrapped function, or can be set through the
        description keyword argument. The description is also updated by arithmetic operations are applied."""
        if self._description is None:
            return callable_name(self.func)
        else:
            return self._description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

    def __call__(self, *x):
        if all(callable(y) for y in x):
            raise NotImplementedError  # this will produce a new MathFunc
        return self.func(*x, *self.args, **self.kwargs)

    def __eq__(self, other):
        try:
            equal = self.description == other.description
        except AttributeError:
            msg = 'Can only compare a MathFunc instance with another MathFunc'
            raise TypeError(msg)

        if not equal:
            msg = 'MathFunc descriptions found to be not equal though may still be equivalent.'
            warn(msg)

        return equal
