import numbers


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

    def __add__(self, other):
        """Add self to a scalar value or any other callable including another MathFunc instance."""
        if callable(other):
            new_func = lambda *x: self(*x) + other(*x)
        elif isinstance(other, numbers.Real):
            new_func = lambda *x: self(*x) + other
        else:
            msg = f"Cannot multiply MathFunc with type {type(other)}. Must be either callable or a scalar value."
            raise TypeError(msg)

        if isinstance(other, MathFunc):
            new_desc = self.description + ' + ' + other.description
        elif callable(other):
            new_desc = self.description + ' + ' + callable_name(other)
        else:
            new_desc = self.description + ' + ' + str(other)

        return MathFunc(func=new_func, description=new_desc)

    def __mul__(self, other):
        """Multiply self with a scalar value or any other callable including another MathFunc instance."""
        if callable(other):
            new_func = lambda *x: self(*x) * other(*x)
        elif isinstance(other, numbers.Real):
            new_func = lambda *x: self(*x) * other
        else:
            msg = f"Cannot multiply MathFunc with type {type(other)}. Must be either callable or a scalar value."
            raise TypeError(msg)

        if isinstance(other, MathFunc):
            new_desc = self.description + ' * ' + other.description
        elif callable(other):
            new_desc = self.description + ' * ' + callable_name(other)
        else:
            new_desc = self.description + ' * ' + str(other)

        return MathFunc(func=new_func, description=new_desc)
