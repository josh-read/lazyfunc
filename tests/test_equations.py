from mfunc import *


@math_func
def one(x):
    return 1


@math_func
def two(x):
    return 2


@math_func
def three(x):
    return 3


def test_equations():
    """Test combining operations of different rank."""
    # no brackets different rank
    eq = one + one / two
    assert str(eq) == 'MathFunc(one + one / two)'
    assert eq(None) == 1 + 1 / 2
    # brackets different rank
    eq = (one + one) / two
    assert str(eq) == 'MathFunc((one + one) / two)'
    assert eq(None) == (1 + 1) / 2
    # brackets different rank
    eq = two + (one + one) / two + three
    assert str(eq) == 'MathFunc(two + (one + one) / two + three)'
    assert eq(None) == 2 + (1 + 1) / 2 + 3
    # brackets different rank
    # eq = (two + (one + one) / two + three) ** two
    # assert str(eq) == 'MathFunc((two + (one + one) / two + three) ** two)'
    # assert eq(None) == (2 + (1 + 1) / 2 + 3) ** 2
