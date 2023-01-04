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


def test_mul():
    # test two LazyFunc objects
    x = np.random.rand(4)
    mf_f = LazyFunc(single_parameter_function)
    mf_h = LazyFunc(SingleParameterClass())
    mf_fh = mf_f * mf_h
    assert str(mf_fh) == 'LazyFunc(single_parameter_function * SingleParameterClass)'
    assert np.allclose(mf_fh(x), x**2)
    # test a LazyFunc object with a normal function
    mf_g = LazyFunc(multi_parameter_function)
    mf_gj = mf_g * MultiParameterClass()
    assert str(mf_gj) == 'LazyFunc(multi_parameter_function * MultiParameterClass)'
    assert np.allclose(mf_gj(x, x), 4*x**2)
    # test a LazyFunc object with a scalar
    mf_f2 = mf_f * 2
    assert str(mf_f2) == 'LazyFunc(single_parameter_function * 2)'
    assert np.allclose(mf_f2(x), 2*x)
    with pytest.raises(TypeError):
        mf_f * 'foo'
    # test LazyFunc operation name and docstring
    assert LazyFunc.__mul__.__name__ == '__mul__'
    assert LazyFunc.__mul__.__doc__ == 'Return new instance LazyFunc(self * other), where other may be a scalar value or any other callable including another LazyFunc instance.'


def test_add():
    # test two LazyFunc objects
    x = np.random.rand(4)
    mf_f = LazyFunc(single_parameter_function)
    mf_h = LazyFunc(SingleParameterClass())
    mf_fh = mf_f + mf_h
    assert str(mf_fh) == 'LazyFunc(single_parameter_function + SingleParameterClass)'
    assert np.allclose(mf_fh(x), 2*x)
    # test a LazyFunc object with a normal function
    mf_g = LazyFunc(multi_parameter_function)
    mf_gj = mf_g + MultiParameterClass()
    assert str(mf_gj) == 'LazyFunc(multi_parameter_function + MultiParameterClass)'
    assert np.allclose(mf_gj(x, x), 4*x)
    # test a LazyFunc object with a scalar
    mf_f2 = mf_f + 2
    assert str(mf_f2) == 'LazyFunc(single_parameter_function + 2)'
    assert np.allclose(mf_f2(x), x + 2)
    with pytest.raises(TypeError):
        mf_f + 'foo'


def test_radd():
    # test two LazyFunc objects
    x = np.random.rand(4)
    mf_f = LazyFunc(single_parameter_function)
    mf_h = LazyFunc(SingleParameterClass())
    mf_fh = mf_f + mf_h
    assert str(mf_fh) == 'LazyFunc(single_parameter_function + SingleParameterClass)'
    assert np.allclose(mf_fh(x), 2*x)
    # test a LazyFunc object with a normal function
    mf_g = LazyFunc(multi_parameter_function)
    mf_jg = MultiParameterClass() + mf_g
    assert str(mf_jg) == 'LazyFunc(MultiParameterClass + multi_parameter_function)'
    assert np.allclose(mf_jg(x, x), 4*x)
    # test a LazyFunc object with a scalar
    mf_2f = 2 + mf_f
    assert str(mf_2f) == 'LazyFunc(2 + single_parameter_function)'
    assert np.allclose(mf_2f(x), x + 2)
    with pytest.raises(TypeError):
        mf_f + 'foo'
