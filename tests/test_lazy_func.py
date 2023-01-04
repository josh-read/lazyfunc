import numpy as np
import pytest

from lazyfunc import LazyFunc


def single_parameter_function(x):
    return x


def multi_parameter_function(x, y):
    return x + y


class SingleParameterClass:

    def __call__(self, x):
        return x


class MultiParameterClass:

    def __call__(self, x, y):
        return x + y


def test_repr():
    mf_f = LazyFunc(single_parameter_function)
    assert str(mf_f) == 'LazyFunc(single_parameter_function)'
    mf_f_with_desc = LazyFunc(single_parameter_function, description='my_single_parameter_function')
    assert str(mf_f_with_desc) == 'LazyFunc(my_single_parameter_function)'
    mf_j = LazyFunc(MultiParameterClass())
    assert str(mf_j) == 'LazyFunc(MultiParameterClass)'

    @LazyFunc
    def abc(x):
        return x

    assert str(abc + abc) == 'LazyFunc(abc + abc)'


def test_call():
    x = np.array([1, 2, 3, 4])
    y = np.random.rand(4)
    print(y)
    mf_f = LazyFunc(single_parameter_function)
    assert np.allclose(mf_f(x), x)
    mf_j = LazyFunc(MultiParameterClass())
    assert np.allclose(mf_j(x, y), (x + y))
    mf = LazyFunc(single_parameter_function)
    mf = mf(SingleParameterClass())
    assert np.allclose(mf(x), x)
    mf_min = LazyFunc(min)
    mf_min_f = mf_min(mf_f) * 2
    assert mf_min_f(x) == min(x) * 2


def test_equality():
    mf_single_parameter_function = LazyFunc(single_parameter_function)
    mf_single_parameter_class = LazyFunc(SingleParameterClass())
    assert (mf_single_parameter_function + mf_single_parameter_class).is_equal(
        mf_single_parameter_function + mf_single_parameter_class)
    with pytest.warns(UserWarning):
        assert not (mf_single_parameter_function + mf_single_parameter_class).is_equal(
             mf_single_parameter_class + mf_single_parameter_function)
