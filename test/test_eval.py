"""tests for evaluation"""

import pytest

from lispy import compile_bytecode, evaluate


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        # Constants
        (1, 1),
        (5, 5),
        # Variables
        (["val", "x", 1], None),
        (["begin", ["val", "x", 1], "x"], 1),
        (["begin", ["val", "x", 1], ["val", "x", 3], "x"], 3),
        # Builtin Functions
        (["+", 1, 2], 3),
        (["-", 2, 1], 1),
        # Conditionals
        (["if", "true", 1, 2], 1),
        (["if", "false", 1, 2], 2),
        # Conditional Assignment
        (["begin", ["if", "true", ["val", "x", 1], ["val", "x", 2]], "x"], 1),
        (["begin", ["if", "false", ["val", "x", 1], ["val", "x", 2]], "x"], 2),
        # Lambda
        ([["lambda", "x", ["*", "x", 2]], 2], 4),
        # Named Function
        (["begin", ["define", "square", "x", ["*", "x", 2]], ["square", 2]], 4),
        # Factorial
        (
            [
                "begin",
                [
                    "define",
                    "factorial",
                    "n",
                    ["if", ["eq", "n", 1], 1, ["*", ["factorial", ["-", "n", 1]], "n"]],
                ],
                ["factorial", 5],
            ],
            120,
        ),
        # Lists
        (["cons", 1, 2], [1, 2]),
    ],
)
def test_eval(tokens, expected):
    """compile tokens and evaluate bytecode"""
    assert evaluate(compile_bytecode(tokens)) == expected
