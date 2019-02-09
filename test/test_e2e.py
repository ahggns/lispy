"""tests for io"""

import pytest

from lispy import compile_bytecode, evaluate, tokenize, parse


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("1", 1),
        ('"hello world"', "hello world"),
        ('begin (define hello_world () ("hello world")) (hello_world)', "hello world"),
        ("begin (val x 1) x", 1),
        (
            "begin (val n 5) (define factorial n (if (eq n 1) 1 (* (factorial (- n 1)) n))) (factorial n)",
            120,
        ),
        (
            "\n".join(
                (
                    "begin",
                    "(val a 3)",
                    "(val b 2)",
                    "(val c 1)",
                    "(define factorial n (if (eq n 1) 1 (* (factorial (- n 1)) n)))",
                    "(factorial (* (+ a b) c))",
                )
            ),
            120,
        ),
        ("(cons 1 2 3 4 5)", [1, 2, 3, 4, 5]),
        (
            "\n".join(
                (
                    "begin",
                    "(define factorial n (if (eq n 1) 1 (* (factorial (- n 1)) n)))",
                    "(map factorial (cons 1 2 3 4 5))",
                )
            ),
            [1, 2, 6, 24, 120],
        ),
        ("(map + (cons 1 2 3) (cons 4 5 6))", [5, 7, 9]),
        ("(map cons (cons 1 2 3) (cons 4 5 6))", [[1, 4], [2, 5], [3, 6]]),
    ],
)
def test_e2e(code, expected):
    assert evaluate(compile_bytecode(parse(tokenize(code)))) == expected
