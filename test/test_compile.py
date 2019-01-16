"""tests for compilation"""

import pytest

from lispy import compile_bytecode
from lispy.core._instruction import LOAD_CONST, STORE_NAME, LOAD_NAME, \
    MAKE_FUNCTION, CALL_FUNCTION

@pytest.mark.parametrize(('tokens', 'expected'), [
    # Constants
    (1, [LOAD_CONST(1)]),
    (5, [LOAD_CONST(5)]),

    # Variables
    (['val', 'x', 1], [LOAD_CONST(1), STORE_NAME('x')]),
    (['val', 'y', 3], [LOAD_CONST(3), STORE_NAME('y')]),
    ('x', [LOAD_NAME('x')]),

    # Builtin Function
    (['+', 1, 2], [LOAD_NAME('+'),
                   LOAD_CONST(1),
                   LOAD_CONST(2),
                   CALL_FUNCTION(2)]),
    (['+'], [LOAD_NAME('+'), CALL_FUNCTION(0)]),

    # Lambda
    (['lambda', ['x'], ['*', 'x', 2]], [
        LOAD_CONST(tuple('x')),
        LOAD_CONST((LOAD_NAME('*'),
                    LOAD_NAME('x'),
                    LOAD_CONST(2),
                    CALL_FUNCTION(2))),
        MAKE_FUNCTION(1),
    ]),
])
def test_compile(tokens, expected):
    """compile tokens into bytecode"""
    assert compile_bytecode(tokens) == expected
