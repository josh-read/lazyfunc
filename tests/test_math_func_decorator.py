from mfunc import MathFunc


def single_parameter_function(x):
    return x


single_parameter_math_func = MathFunc(single_parameter_function)


@MathFunc
def single_parameter_function(x):
    return x


def test_decorated_function():
    assert single_parameter_math_func == single_parameter_function
