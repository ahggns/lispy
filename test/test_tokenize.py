"""tests for io"""

import pytest

from lispy import tokenize

@pytest.mark.parametrize(('string', 'expected'), [
   ('', []),
   (' ', []),
   ('x', ['x']),
   ('1', ['1']),
   ('2.0', ['2.0']),
   ('f 2', ['f', '2']),
   ('(f)', ['(', 'f', ')']),
   ('(f x)', ['(', 'f', 'x', ')']),
   ('(f 1 2)', ['(', 'f', '1', '2', ')']),
   ('(f "1 2")', ['(', 'f', '"1 2"', ')']),
   ('(f) (x)', ['(', 'f', ')', '(', 'x', ')']),
   ('begin 1 2 3', ['begin', '1', '2', '3'])
])
def test_tokenize(string, expected):
    """assert strings tokenize correctly"""
    assert tokenize(string) == expected
