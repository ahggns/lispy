"""tests for io"""

import pytest

from lispy import parse


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([], []),
        (["x"], "x"),
        (["1"], 1),
        (["2.0"], 2.0),
        (["f", "2"], ["f", 2]),
        (["(", "f", ")"], ["f"]),
        (["(", "f", "x", ")"], ["f", "x"]),
        (["(", "f", "1", "2", ")"], ["f", 1, 2]),
        (["begin", "1", "2", "3"], ["begin", 1, 2, 3]),
    ],
)
def test_parse(tokens, expected):
    """assert tokens parse correctly"""
    assert parse(tokens) == expected
