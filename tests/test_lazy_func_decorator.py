from lazyfunc import LazyFunc


def single_parameter_function(x):
    return x


single_parameter_math_func = LazyFunc(single_parameter_function)


@LazyFunc
def single_parameter_function(x):
    return x


def test_decorated_function():
    assert single_parameter_math_func == single_parameter_function
