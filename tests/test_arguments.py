import inspect

import pytest

from lazyfunc import LazyFunc


def square(x, *, foo=2):
    return x ** 2 + foo


lf_square = LazyFunc(square)


def cube(x, /, bar):
    return x ** 3 + bar


def test_signature_propagation_1():
    assert inspect.signature(square) == inspect.signature(lf_square)


def test_signature_propagation_2():
    assert inspect.signature(square) == inspect.signature(~lf_square)


def test_signature_combination():
    assert inspect.signature(lf_square + cube).parameters.keys() == {'x', 'foo', 'bar'}


def test_combined_keywords():
    f = lf_square + cube
    assert f(2, foo=1, bar=2) == 15
    assert f(2, bar=2) == 16
    with pytest.raises(TypeError):
        f(2, foo=1)
    with pytest.raises(TypeError):
        f(2, 2, foo=1)
