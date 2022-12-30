"""Test combining operations of different rank."""


from mfunc import *


@MathFunc
def one(x):
    return 1


@MathFunc
def two(x):
    return 2


@MathFunc
def three(x):
    return 3


def test_equation_1():
    eq = one + one / two
    assert str(eq) == 'MathFunc(one + one / two)'
    assert eq(None) == 1 + 1 / 2


def test_equation_2():
    eq = (one + one) / two
    assert str(eq) == 'MathFunc((one + one) / two)'
    assert eq(None) == (1 + 1) / 2


def test_equation_3():
    eq = two + (one + one) / two + three
    assert str(eq) == 'MathFunc(two + (one + one) / two + three)'
    assert eq(None) == 2 + (1 + 1) / 2 + 3


def test_equation_4():
    eq = (two + (one + one) / two + three) ** two
    assert str(eq) == 'MathFunc((two + (one + one) / two + three) ** two)'
    assert eq(None) == (2 + (1 + 1) / 2 + 3) ** 2


def test_equation_5():
    eq = ((one + one) * two / two) ** (three / one) + one
    assert str(eq) == 'MathFunc(((one + one) * two / two) ** (three / one) + one)'
    assert eq(None) == ((1 + 1) * 2 / 2) ** (3 / 1) + 1
