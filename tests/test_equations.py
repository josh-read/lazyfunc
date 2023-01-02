"""Test that combining operations of different precedence returns the correct result and also has the
correct placement of parentheses in the description."""

import pytest

from mfunc import *
from mfunc.utils import add_parentheses


@MathFunc
def one(x):
    return 1


@MathFunc
def two(x):
    return 2


@MathFunc
def three(x):
    return 3


@pytest.mark.parametrize(
    'equation',
[
    '1 + 1 / 2',
    '(1 + 1) / 2',
    '2 + (1 + 1) / 2 + 3',
    '(2 + (1 + 1) / 2 + 3) ** 2',
    '((1 + 1) * 2 / 2) ** (3 / 1) + 1',
    '-(1 + 1) / 2',
    '+(1 + 1) / 2',
    '~(1 + 1) / 2',
    '3 >> 2 // 2',
    '(1 << 3) / 2',
    '1 & 2 // 2',
    '(1 & 2) // 2',
    '1 ^ 2 // 2',
    '(1 ^ 2) // 2',
    '1 | 2 // 2',
    '(1 | 2) // 2',
])
def test_equation(equation):
    equation_from_math_funcs = equation.replace('1', 'one').replace('2', 'two').replace('3', 'three')
    mf = eval(equation_from_math_funcs)
    mf_str = 'MathFunc' + add_parentheses(equation_from_math_funcs)
    assert mf(None) == eval(equation)
    assert str(mf) == mf_str
