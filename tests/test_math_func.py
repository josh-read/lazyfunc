import numpy as np
import pytest

from mfunc import MathFunc


def f(x):
    return x


def g(x, y):
    return x + y


class H:

    def __call__(self, x):
        return x


class J:

    def __call__(self, x, y):
        return x + y


def test_repr():
    mf_f = MathFunc(f)
    assert str(mf_f) == 'MathFunc(f)'
    mf_f_with_desc = MathFunc(f, description='my_function')
    assert str(mf_f_with_desc) == 'MathFunc(my_function)'
    mf_j = MathFunc(J())
    assert str(mf_j) == 'MathFunc(J)'


def test_call():
    x = np.array([1, 2, 3, 4])
    y = np.random.rand(4)
    print(y)
    mf_f = MathFunc(f)
    assert np.allclose(mf_f(x), x)
    mf_j = MathFunc(J())
    assert np.allclose(mf_j(x, y), (x + y))


def test_mul():
    # test two MathFunc objects
    x = np.random.rand(4)
    mf_f = MathFunc(f)
    mf_h = MathFunc(H())
    mf_fh = mf_f * mf_h
    assert str(mf_fh) == 'MathFunc(f * H)'
    assert np.allclose(mf_fh(x), x**2)
    # test a MathFunc object with a normal function
    mf_g = MathFunc(g)
    mf_gj = mf_g * J()
    assert str(mf_gj) == 'MathFunc(g * J)'
    assert np.allclose(mf_gj(x, x), 4*x**2)
    # test a MathFunc object with a scalar
    mf_f2 = mf_f * 2
    assert str(mf_f2) == 'MathFunc(f * 2)'
    assert np.allclose(mf_f2(x), 2*x)
    with pytest.raises(TypeError):
        mf_f * 'foo'
    # test MathFunc operation name and docstring
    assert MathFunc.__mul__.__name__ == '__mul__'
    assert MathFunc.__mul__.__doc__ == 'Return new MathFunc with unevaluated function resulting from self * other, where other may be a scalar value or any other callable including another MathFunc instance.'


def test_add():
    # test two MathFunc objects
    x = np.random.rand(4)
    mf_f = MathFunc(f)
    mf_h = MathFunc(H())
    mf_fh = mf_f + mf_h
    assert str(mf_fh) == 'MathFunc(f + H)'
    assert np.allclose(mf_fh(x), 2*x)
    # test a MathFunc object with a normal function
    mf_g = MathFunc(g)
    mf_gj = mf_g + J()
    assert str(mf_gj) == 'MathFunc(g + J)'
    assert np.allclose(mf_gj(x, x), 4*x)
    # test a MathFunc object with a scalar
    mf_f2 = mf_f + 2
    assert str(mf_f2) == 'MathFunc(f + 2)'
    assert np.allclose(mf_f2(x), x + 2)
    with pytest.raises(TypeError):
        mf_f + 'foo'


def test_truediv():
    x = 1
    mf_f = MathFunc(f)
    tricky_eq1 = mf_f + mf_f / (mf_f + 2)
    expected_str1 = 'MathFunc(f + (f) / (f + 2))'
    assert np.allclose(tricky_eq1(x), x + x / (x + 2))
    assert str(tricky_eq1) == expected_str1
    tricky_eq2 = (mf_f + mf_f) / (mf_f + 2)
    expected_str2 = 'MathFunc((f + f) / (f + 2))'
    assert np.allclose(tricky_eq2(x), (x + x) / (x + 2))
    assert str(tricky_eq2) == expected_str2
