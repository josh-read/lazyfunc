import inspect
from warnings import warn

from lazyfunc.arguments import ARGUMENT_ORDER
from lazyfunc.operators import operators
from lazyfunc.utils import callable_name, add_parentheses, insert


class LazyFuncMeta(type):
    def __new__(mcs, name, bases, attrs):
        for operator in operators:
            attrs[operator.name] = mcs.lazy_func_method_factory(operator)
            if operator.has_reverse:
                reverse_operator_name = insert(operator.name, "r", index=2)
                attrs[reverse_operator_name] = mcs.lazy_func_method_factory(
                    operator, reverse=True
                )
        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def lazy_func_method_factory(operator, reverse=False):
        """Function factory which produces the functions for operations which are bound
        to LazyFunc."""

        def inner(*instances):
            new_func = LazyFuncMeta.new_function(operator, *instances)
            new_func.__signature__ = LazyFuncMeta.build_new_signature(instances)
            new_desc = LazyFuncMeta.description_from_operator(
                operator, *instances, reverse=reverse
            )
            mf = LazyFunc(func=new_func, description=new_desc)
            mf._precedence = operator.precedence
            return mf

        if operator.number_of_operands == 1:
            operation_description = operator.format("self")
        elif operator.number_of_operands == 2:
            if reverse:
                operation_description = operator.format("other", "self")
            else:
                operation_description = operator.format("self", "other")

        inner.__name__ = operator.name
        inner.__doc__ = (
            f"Return new instance LazyFunc({operation_description}), "
            "where other may be a scalar value or any other callable including another LazyFunc instance."
        )
        return inner

    @staticmethod
    def new_function(operator, *instances):
        def inner(*args, **kwargs):
            operator_args = []
            for obj in instances:
                if not callable(obj):
                    operator_args.append(obj)
                else:
                    callable_kwargs = {}
                    for key in kwargs:
                        if key in inspect.signature(obj).parameters:
                            callable_kwargs[key] = kwargs[key]
                    operator_args.append(obj(*args, **callable_kwargs))
            return operator.func(*operator_args)

        return inner

    @staticmethod
    def description_from_operator(operator, *instances, reverse):
        """Returns a string describing the function resulting from combining self and other through
        the specified operation. The precedence of the operation is compared to the precedence of the last operation
        on self and other to determine whether parentheses are required."""
        descriptions = [
            LazyFuncMeta._get_desc(instance, operator.precedence)
            for instance in instances
        ]

        if reverse:
            descriptions = reversed(descriptions)
        return operator.format(*descriptions)

    @staticmethod
    def _get_desc(instance, operator_precedence):
        if callable(instance):
            desc = callable_name(instance)
        else:
            desc = str(instance)

        precedence = getattr(instance, "_precedence", None)
        if precedence is None:
            pass
        elif precedence < operator_precedence:
            desc = add_parentheses(desc)

        return desc

    @staticmethod
    def build_new_signature(instances):
        callables = [obj for obj in instances if callable(obj)]
        if len(callables) == 1:
            return instances[0].__signature__
        else:  # build new signature merging any duplicated arguments
            combined_params = {}
            instance_parameters = [
                inspect.signature(obj).parameters for obj in callables
            ]
            for (
                kind
            ) in (
                ARGUMENT_ORDER
            ):  # positional arguments must come first, default arguments must come last
                for (
                    params
                ) in (
                    instance_parameters
                ):  # arguments of same kind from first instance come before last instance
                    for name, param in params.items():
                        if param.kind == kind and name not in combined_params:
                            combined_params[name] = param
            return inspect.Signature(parameters=combined_params.values())


class LazyFunc(metaclass=LazyFuncMeta):
    """Wrap a callable object enabling arithmetic operations between it and scalar values or any other callables,
    including LazyFunc instances."""

    def __init__(self, func, description=None, **kwargs):
        self.func = func
        self._description = description
        self._kwargs = self._default_kwargs = kwargs
        self._precedence = None

    @property
    def __signature__(self):
        return inspect.signature(self.func)

    @property
    def description(self) -> str:
        """Defaults to the name of the wrapped callable, but can be set by the user at object initialisation. Also
        updated when operations are applied with other callables.

        Examples:
            >>> def my_function(x):
            ...     return x
            >>> lf_auto = LazyFunc(my_function)
            >>> lf_auto.description
            'my_function'
            >>> lf_named = LazyFunc(my_function, description='my_named_function')
            >>> lf_named.description
            'my_named_function'

        Returns:
            A string describing the wrapped function.
        """
        if self._description is None:
            return callable_name(self.func)
        else:
            return self._description

    @property
    def __name__(self) -> str:
        """Alias of the LazyFunc description."""
        return self.description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

    def __call__(self, *args, **kwargs) -> object:
        """Either calls the wrapped function with the provided args and kwargs, or if the first argument is a callable,
        returns a new LazyFunc object of LazyFunc(args[0](self)).

        When calling a LazyFunc instance, if the first argument is NOT a callable, it behaves exactly as the unwrapped
        callable.
        Examples:
            >>> @LazyFunc
            ... def my_function(x):
            ...     return 2 * x
            ...
            >>> my_function('foo')  # first argument is not callable
            'foofoo'
            >>> import builtins
            >>> builtin_min = builtins.min
            >>> min = LazyFunc(min)
            >>> min([3, 1, 4, 1, 5, 9])  # first argument is not callable
            1
            >>> min('lazy', 'function', key=lambda s: s[1])  # first argument is not callable
            'lazy'
            >>> min_of_my_function = min(my_function)  # first argument is callable
            >>> min_of_my_function
            LazyFunc(min(my_function))

        Args:
            args: Positional arguments to be passed to wrapped function.
            kwargs: Keyword arguments to be passed to wrapped function.

        Returns:
            Either the result of the wrapped function evaluated with the supplied args and _kwargs, or a new LazyFunc
            instance.
        """
        if callable(args[0]):
            operator_precedence = 17
            other_func, *args = args
            new_func = lambda *y: self.func(other_func(*y), *args, **kwargs)
            new_desc = (
                LazyFuncMeta._get_desc(self, operator_precedence)
                + "("
                + callable_name(other_func)
                + ")"
            )
            mf = LazyFunc(func=new_func, description=new_desc)
            mf._precedence = operator_precedence
            return mf
        else:  # when the function is called the kwargs supplied to the call take precedence over those set elsewhere
            final_kwargs = self._kwargs | kwargs
            return self.func(*args, **final_kwargs)

    def set_kwargs(self, **kwargs):
        self._kwargs = kwargs
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._kwargs = self._default_kwargs

    def is_equal(self, other: callable) -> bool:
        """Checks for equality between self and other.

        To stay consistent with LazyFunc's other dunder methods, the `__eq__` method lazily compares equality
        between the wrapped LazyFunc and other. Therefore, this method exists to check whether two unevaluated
        LazyFunc objects are equal, without calling them and comparing the results.

        Examples:
            >>> def my_function(x):
            ...     return x
            >>> lf_auto_1 = LazyFunc(my_function)
            >>> lf_auto_2 = LazyFunc(my_function)
            >>> lf_named = LazyFunc(my_function, description='my_named_function')
            >>> lf_auto_1.is_equal(lf_auto_2)
            True
            >>> lf_auto_1.is_equal(lf_named)
            False
        """
        try:
            equal = self.description == other.description
        except AttributeError:
            msg = "Can only compare a LazyFunc instance with another LazyFunc"
            raise TypeError(msg)

        if not equal:
            msg = "LazyFunc descriptions found to be not equal though may still be equivalent."
            warn(msg)

        return equal
