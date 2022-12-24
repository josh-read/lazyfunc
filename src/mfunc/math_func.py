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


def new_description_from_operation(self, other, operation_symbol, commutative):
    self_desc = self.description
    if isinstance(other, MathFunc):
        other_desc = other.description
    elif callable(other):
        other_desc = callable_name(other)
    else:
        other_desc = str(other)

    if not commutative:
        # Adding brackets around each operand is the only way to ensure correctness with the current implementation.
        # However, it is not desirable as it produces a bunch of unnecessary brackets. This problem can be alleviated
        # if this function had knowledge of all previous operations.
        self_desc, other_desc = [add_parentheses(desc) for desc in (self_desc, other_desc)]

    return ' '.join((self_desc, operation_symbol, other_desc))


def math_operation(operation, operation_symbol, commutative):
    def inner(self, other):
        new_func = new_func_from_operation(self, other, operation)
        new_desc = new_description_from_operation(self, other, operation_symbol, commutative)
        return MathFunc(func=new_func, description=new_desc)
    return inner


class MathFunc:

    __add__ = math_operation(operator.add, '+', True)
    __mul__ = math_operation(operator.mul, '*', True)
    __truediv__ = math_operation(operator.truediv, '/', False)

    def __init__(self, func, *args, description=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description

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
