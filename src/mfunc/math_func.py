import numbers
from warnings import warn

from mfunc.utils import callable_name, add_parentheses, insert
from mfunc.operators import operators


def function_from_unary_operator(self, operator):
    return lambda *x: operator.func(self(*x))


def function_from_dyadic_operator(self, other, operator):
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


def description_from_unary_operator(self, operator):
    self_desc = self.description
    self_rank = getattr(self, '_precedence')
    if self_rank is None:
        pass
    elif self_rank < operator.precedence:
        self_desc = add_parentheses(self_desc)
    return operator.format(self_desc)


def description_from_dyadic_operator(self, other, operator, reverse):
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
        return operator.format(other_desc, self_desc)
    else:
        return operator.format(self_desc, other_desc)


def math_func_unary_method_factory(operator):
    """Function factory which produces the functions for operations which are bound
    to MathFunc."""

    def inner(self):
        new_func = function_from_unary_operator(self, operator)
        new_desc = description_from_unary_operator(self, operator)
        mf = MathFunc(func=new_func, description=new_desc)
        mf._precedence = operator.precedence
        return mf

    operation_description = operator.format('self')

    inner.__name__ = operator.name
    inner.__doc__ = f"Return new instance MathFunc({operation_description}), " \
                    "where other may be a scalar value or any other callable including another MathFunc instance."
    return inner


def math_func_dyadic_method_factory(operator, reverse=False):
    """Function factory which produces the functions for operations which are bound
    to MathFunc."""

    def inner(self, other):
        new_func = function_from_dyadic_operator(self, other, operator)
        new_desc = description_from_dyadic_operator(self, other, operator, reverse)
        mf = MathFunc(func=new_func, description=new_desc)
        mf._precedence = operator.precedence
        return mf

    if reverse:
        operation_description = operator.format('other', 'self')
    else:
        operation_description = operator.format('self', 'other')

    inner.__name__ = operator.name
    inner.__doc__ = f"Return new instance MathFunc({operation_description}), " \
                    "where other may be a scalar value or any other callable including another MathFunc instance."
    return inner


def math_func_meta(name, bases, attrs):
    """Metaclass over class decorator as special operator behaviour needs to persist through inheritance."""
    for operator in operators:
        if operator.number_of_operands == 1:
            attrs[operator.name] = math_func_unary_method_factory(operator)
        if operator.number_of_operands == 2:
            attrs[operator.name] = math_func_dyadic_method_factory(operator)
        if operator.has_reverse:
            reverse_operator_name = insert(operator.name, 'r', index=2)
            attrs[reverse_operator_name] = math_func_dyadic_method_factory(operator, reverse=True)
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

    def is_equal(self, other):
        """To stay consistent with all other dunder methods, the __eq__ method lazily compares equality
        between the wrapped MathFunc and other. Therefore, this method exists to check whether two unevaluated
        MathFunc objects are equal, without calling them and comparing the results."""
        try:
            equal = self.description == other.description
        except AttributeError:
            msg = 'Can only compare a MathFunc instance with another MathFunc'
            raise TypeError(msg)

        if not equal:
            msg = 'MathFunc descriptions found to be not equal though may still be equivalent.'
            warn(msg)

        return equal
