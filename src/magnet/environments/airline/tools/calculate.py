"""Adapted from τ-bench https://arxiv.org/abs/2406.12045"""


def calculate(expression: str) -> str:
    """
    Calculate the result of a mathematical expression.

    Args:
        expression: The mathematical expression to calculate, such as '2 + 2'.
                   The expression can contain numbers, operators (+, -, *, /),
                   parentheses, and spaces.

    Returns:
        The calculated result as a string, rounded to 2 decimal places,
        or an error message.
    """
    if not all(char in "0123456789+-*/(). " for char in expression):
        return "Error: invalid characters in expression"
    try:
        return str(round(float(eval(expression, {"__builtins__": None}, {})), 2))
    except Exception as e:
        return f"Error: {e}"
