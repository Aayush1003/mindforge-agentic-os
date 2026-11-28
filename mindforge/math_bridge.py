"""A small, deterministic bridge from arithmetic expressions to exact results.

This module deliberately handles a tiny language rather than executing Python:
integer literals, parentheses, unary +/-, and +, -, *, /, **. Results are exact
rational numbers; the decimal rendering is for display, not proof.
"""

from __future__ import annotations

import ast
from decimal import Decimal, localcontext
from fractions import Fraction
import operator

_MAX_EXPRESSION_LENGTH = 256
_MAX_AST_NODES = 64
_MAX_EXPONENT = 32
_MAX_RESULT_BITS = 4096
_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _evaluate(node: ast.AST) -> Fraction:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return Fraction(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow):
            if right.denominator != 1 or abs(right.numerator) > _MAX_EXPONENT:
                raise ValueError(f"exponent must be an integer between -{_MAX_EXPONENT} and {_MAX_EXPONENT}")
            result = left ** right.numerator
        else:
            result = _BINARY_OPERATORS[type(node.op)](left, right)
        if result.numerator.bit_length() > _MAX_RESULT_BITS or result.denominator.bit_length() > _MAX_RESULT_BITS:
            raise ValueError("exact result exceeds the supported size limit")
        return result
    raise ValueError("expression contains an unsupported construct")


def evaluate_expression(expression: str) -> dict[str, str]:
    """Evaluate a bounded arithmetic expression and return a traceable result.

    No names, function calls, attributes, floats, or Python execution are
    accepted. The exact value is returned as a reduced numerator/denominator;
    the decimal value is rounded to 28 significant digits for display.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("expression must be a non-empty string")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise ValueError(f"expression must be at most {_MAX_EXPRESSION_LENGTH} characters")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise ValueError("expression is not valid arithmetic syntax") from error
    if sum(1 for _ in ast.walk(tree)) > _MAX_AST_NODES:
        raise ValueError(f"expression must contain at most {_MAX_AST_NODES} syntax nodes")

    try:
        result = _evaluate(tree)
    except ZeroDivisionError as error:
        raise ValueError("division by zero is undefined") from error

    with localcontext() as context:
        context.prec = 28
        decimal_value = Decimal(result.numerator) / Decimal(result.denominator)

    return {
        "expression": expression,
        "exact": str(result.numerator) if result.denominator == 1 else f"{result.numerator}/{result.denominator}",
        "decimal": str(decimal_value),
        "status": "exact_rational_calculation",
        "scope": "Evaluates arithmetic only; this is not a symbolic proof or a scientific discovery.",
    }
