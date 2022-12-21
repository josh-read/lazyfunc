import numpy as np

from mfunc import MathFunc


def f(x):
    return x


class G:

    def __call__(self, x, y):
        return x + y


def test_repr():
    mf_f = MathFunc(f)
    assert str(mf_f) == 'MathFunc(f)'
    mf_g = MathFunc(G())
    assert str(mf_g) == 'MathFunc(G)'


def test_call():
    x = np.array([1, 2, 3, 4])
    y = np.random.rand(4)
    print(y)
    mf_f = MathFunc(f)
    assert np.allclose(mf_f(x), x)
    mf_g = MathFunc(G())
    assert np.allclose(mf_g(x, y), (x + y))
