import numbers
from warnings import warn

from lazyfunc.utils import callable_name, add_parentheses, insert
from lazyfunc.operators import operators


def function_from_operator(operator, *instances):
    """Returns a function by combining self and other through a specified operation.
    Self must be of type LazyFunc, other may be a scalar value or any callable including LazyFunc"""
    if operator.number_of_operands == 1:
        self, = instances
        return lambda *x: operator.func(self(*x))
    elif operator.number_of_operands == 2:
        self, other = instances
        if callable(other):
            return lambda *x: operator.func(self(*x), other(*x))
        elif isinstance(other, numbers.Real):
            return lambda *x: operator.func(self(*x), other)
        else:
            msg = f"Cannot call {operator.name} on LazyFunc and type {type(other)}. " \
                  f"Must be either callable or a scalar value."
            raise TypeError(msg)
    else:
        msg = 'Handling of ternary operators not yet implemented!'
        raise NotImplementedError(msg)


def _get_desc(instance, operator_precedence):
    if isinstance(instance, LazyFunc):
        desc = instance.description
    elif callable(instance):
        desc = callable_name(instance)
    else:
        desc = str(instance)

    precedence = getattr(instance, '_precedence', None)
    if precedence is None:
        pass
    elif precedence < operator_precedence:
        desc = add_parentheses(desc)

    return desc


def description_from_operator(operator, *instances, reverse):
    """Returns a string describing the function resulting from combining self and other through
    the specified operation. The precedence of the operation is compared to the precedence of the last operation
    on self and other to determine whether parentheses are required."""
    descriptions = [_get_desc(instance, operator.precedence) for instance in instances]

    if reverse:
        descriptions = reversed(descriptions)
    return operator.format(*descriptions)


def lazy_func_method_factory(operator, reverse=False):
    """Function factory which produces the functions for operations which are bound
    to LazyFunc."""

    def inner(*instances):
        new_func = function_from_operator(operator, *instances)
        new_desc = description_from_operator(operator, *instances, reverse=reverse)
        mf = LazyFunc(func=new_func, description=new_desc)
        mf._precedence = operator.precedence
        return mf

    if operator.number_of_operands == 1:
        operation_description = operator.format('self')
    elif operator.number_of_operands == 2:
        if reverse:
            operation_description = operator.format('other', 'self')
        else:
            operation_description = operator.format('self', 'other')

    inner.__name__ = operator.name
    inner.__doc__ = f"Return new instance LazyFunc({operation_description}), " \
                    "where other may be a scalar value or any other callable including another LazyFunc instance."
    return inner


def lazy_func_meta(name, bases, attrs):
    """Metaclass over class decorator as special operator behaviour needs to persist through inheritance."""
    for operator in operators:
        attrs[operator.name] = lazy_func_method_factory(operator)
        if operator.has_reverse:
            reverse_operator_name = insert(operator.name, 'r', index=2)
            attrs[reverse_operator_name] = lazy_func_method_factory(operator, reverse=True)
    return type(name, bases, attrs)


class LazyFunc(metaclass=lazy_func_meta):
    """Wrap a callable object enabling arithmetic operations between it and scalar values or any other callables,
    including LazyFunc instances."""

    def __init__(self, func, *args, description=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description
        self._precedence = None

    @property
    def description(self):
        """Description of the function wrapped by the LazyFunc. This information is presented in the
        __repr__. This defaults to the __name__ of the wrapped function, or can be set through the
        description keyword argument. The description is also updated by arithmetic operations are applied."""
        if self._description is None:
            return callable_name(self.func)
        else:
            return self._description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

    def __call__(self, *args, **kwargs):
        if callable(args[0]):
            operator_precedence = 17
            other_func, *args = args
            new_func = lambda *y: self.func(other_func(*y), *args, **kwargs)
            if isinstance(other_func, LazyFunc):
                new_desc = _get_desc(self, operator_precedence) + _get_desc(other_func, operator_precedence)
            else:
                new_desc = _get_desc(self, operator_precedence) + '(' + callable_name(other_func) + ')'
            mf = LazyFunc(func=new_func, description=new_desc)
            mf._precedence = operator_precedence
            return mf
        else:
            return self.func(*args, *self.args, **kwargs, **self.kwargs)

    def is_equal(self, other):
        """To stay consistent with all other dunder methods, the __eq__ method lazily compares equality
        between the wrapped LazyFunc and other. Therefore, this method exists to check whether two unevaluated
        LazyFunc objects are equal, without calling them and comparing the results."""
        try:
            equal = self.description == other.description
        except AttributeError:
            msg = 'Can only compare a LazyFunc instance with another LazyFunc'
            raise TypeError(msg)

        if not equal:
            msg = 'LazyFunc descriptions found to be not equal though may still be equivalent.'
            warn(msg)

        return equal
