import numbers
from warnings import warn

from mfunc.utils import callable_name, add_parentheses, insert
from mfunc.operators import operators


def new_func_from_operation(self, other, operator):
    """Returns a function by combining self and other through a specified operation.
    Self must be of type MathFunc, other may be a scalar value or any callable including MathFunc"""
    if callable(other):
        return lambda *x: operator.func(self(*x), other(*x))
    elif isinstance(other, numbers.Real):
        return lambda *x: operator.func(self(*x), other)
    else:
        msg = f"Cannot call {operator.name} on MathFunc and type {type(other)}. " \
              f"Must be either callable or a scalar value."
        raise TypeError(msg)


def new_description_from_operation(self, other, operator, reverse):
    """Returns a string describing the function resulting from combining self and other through
    the specified operation. The precedence of the operation is compared to the precedence of the last operation
    on self and other to determine whether parentheses are required."""
    self_desc = self.description
    if isinstance(other, MathFunc):
        other_desc = other.description
    elif callable(other):
        other_desc = callable_name(other)
    else:
        other_desc = str(other)

    self_rank = getattr(self, '_precedence')
    if self_rank is None:
        pass
    elif self_rank < operator.precedence:
        self_desc = add_parentheses(self_desc)

    other_rank = getattr(other, '_precedence', None)  # if other is not a MathFunc, it will not have a precedence attribute
    if other_rank is None:
        pass
    elif other_rank < operator.precedence:
        other_desc = add_parentheses(other_desc)

    if reverse:
        return operator.operation_format_template.format(other_desc, self_desc)
    else:
        return operator.operation_format_template.format(self_desc, other_desc)


def math_operation(operator, reverse=False):
    """Function generator which produces the functions for arithmetic operations which are bound
    to MathFunc."""

    def inner(self, other):
        new_func = new_func_from_operation(self, other, operator)
        new_desc = new_description_from_operation(self, other, operator, reverse)
        mf = MathFunc(func=new_func, description=new_desc)
        mf._precedence = operator.precedence
        return mf

    if reverse:
        operation_description = operator.operation_format_template.format('other', 'self')
    else:
        operation_description = operator.operation_format_template.format('self', 'other')

    inner.__name__ = operator.name
    inner.__doc__ = f"Return new instance MathFunc({operation_description}), " \
                    "where other may be a scalar value or any other callable including another MathFunc instance."
    return inner


def math_func_meta(name, bases, attrs):
    """Metaclass over class decorator as special operator behaviour needs to persist through inheritance."""
    for operator in operators:
        attrs[operator.name] = math_operation(operator)
        if operator.number_of_operands == 2:  # dyadic operators all have reverse methods
            reverse_operator_name = insert(operator.name, 'r', index=2)
            attrs[reverse_operator_name] = math_operation(operator, reverse=True)
    return type(name, bases, attrs)


class MathFunc(metaclass=math_func_meta):
    """Wrap a callable object enabling arithmetic operations between it and scalar values or any other callables,
    including MathFunc instances."""

    def __init__(self, func, *args, description=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description
        self._precedence = None

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
