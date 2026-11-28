from fractions import Fraction

import pytest

from mindforge.math_bridge import evaluate_expression


def test_expression_returns_exact_and_display_values():
    result = evaluate_expression("(1 + 2) / 6")

    assert result["exact"] == "1/2"
    assert result["decimal"] == "0.5"
    assert result["status"] == "exact_rational_calculation"


def test_integer_power_and_negative_exponent_are_exact():
    assert evaluate_expression("2 ** 10")["exact"] == "1024"
    assert evaluate_expression("2 ** -3")["exact"] == "1/8"


@pytest.mark.parametrize(
    "expression",
    ["__import__('os')", "1.5 + 2", "x + 1", "2 ** 33", "1 / 0"],
)
def test_rejects_unsupported_or_unsafe_expressions(expression):
    with pytest.raises(ValueError):
        evaluate_expression(expression)


def test_rejects_oversized_expressions():
    with pytest.raises(ValueError, match="at most"):
        evaluate_expression("1 + " + "1 + " * 100 + "1")


def test_fraction_representation_is_reduced():
    result = evaluate_expression("6 / 8")
    assert Fraction(result["exact"]) == Fraction(3,  4)
