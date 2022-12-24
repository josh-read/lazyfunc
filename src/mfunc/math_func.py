import numbers
import operator


def callable_name(func):
    try:
        return func.__name__
    except AttributeError:
        return func.__class__.__name__


def add_parentheses(s):
    return ''.join(['(', s, ')'])


class MathFunc:

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

    def __add__(self, other):
        """Add self to a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.add)
        new_desc = self.new_description_from_operation(other, '+', commutative=True)
        return MathFunc(func=new_func, description=new_desc)

    def __mul__(self, other):
        """Multiply self with a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.mul)
        new_desc = self.new_description_from_operation(other, '*', commutative=True)
        return MathFunc(func=new_func, description=new_desc)

    def __truediv__(self, other):
        """Multiply self with a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.truediv)
        new_desc = self.new_description_from_operation(other, '/', commutative=False)
        return MathFunc(func=new_func, description=new_desc)
