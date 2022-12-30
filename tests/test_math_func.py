import numpy as np
import pytest

from mfunc import MathFunc


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
    mf_f = MathFunc(single_parameter_function)
    assert str(mf_f) == 'MathFunc(single_parameter_function)'
    mf_f_with_desc = MathFunc(single_parameter_function, description='my_single_parameter_function')
    assert str(mf_f_with_desc) == 'MathFunc(my_single_parameter_function)'
    mf_j = MathFunc(MultiParameterClass())
    assert str(mf_j) == 'MathFunc(MultiParameterClass)'


def test_call():
    x = np.array([1, 2, 3, 4])
    y = np.random.rand(4)
    print(y)
    mf_f = MathFunc(single_parameter_function)
    assert np.allclose(mf_f(x), x)
    mf_j = MathFunc(MultiParameterClass())
    assert np.allclose(mf_j(x, y), (x + y))
    with pytest.raises(NotImplementedError):
        mf = MathFunc(single_parameter_function)
        mf = mf(SingleParameterClass())
        assert mf(x) == x


def test_equality():
    mf_single_parameter_function = MathFunc(single_parameter_function)
    mf_single_parameter_class = MathFunc(SingleParameterClass())
    assert (mf_single_parameter_function + mf_single_parameter_class
            == mf_single_parameter_function + mf_single_parameter_class)
    with pytest.warns(UserWarning):
        assert (mf_single_parameter_function + mf_single_parameter_class
                != mf_single_parameter_class + mf_single_parameter_function)
