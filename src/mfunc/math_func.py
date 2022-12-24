import numbers
import operator


def callable_name(func):
    try:
        return func.__name__
    except AttributeError:
        return func.__class__.__name__


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

    def __add__(self, other):
        """Add self to a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.add)

        if isinstance(other, MathFunc):
            new_desc = self.description + ' + ' + other.description
        elif callable(other):
            new_desc = self.description + ' + ' + callable_name(other)
        else:
            new_desc = self.description + ' + ' + str(other)

        return MathFunc(func=new_func, description=new_desc)

    def __mul__(self, other):
        """Multiply self with a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.mul)

        if isinstance(other, MathFunc):
            new_desc = self.description + ' * ' + other.description
        elif callable(other):
            new_desc = self.description + ' * ' + callable_name(other)
        else:
            new_desc = self.description + ' * ' + str(other)

        return MathFunc(func=new_func, description=new_desc)

    def __truediv__(self, other):
        """Multiply self with a scalar value or any other callable including another MathFunc instance."""
        new_func = self.new_func_from_operation(other, operator.truediv)

        # Adding brackets around each operand is the only way to ensure correctness with the current implementation.
        # However, it is not desirable as it produces a bunch of unnecessary brackets. This problem can be alleviated
        # if this function had knowledge of all previous operations.
        if isinstance(other, MathFunc):
            new_desc = '(' + self.description + ') / (' + other.description + ')'
        elif callable(other):
            new_desc = '(' + self.description + ') / (' + callable_name(other) + ')'
        else:
            new_desc = '(' + self.description + ') / (' + str(other) + ')'

        return MathFunc(func=new_func, description=new_desc)
