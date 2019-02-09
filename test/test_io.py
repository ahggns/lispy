"""tests for io"""

import io
from contextlib import redirect_stdout
import pytest
from lispy.io import (
    deserialize_bytecode,
    execute_file,
    serialize_bytecode,
    save_bytecode,
    load_bytecode,
)
from lispy.core._instruction import (
    LOAD_CONST,
    STORE_NAME,
    LOAD_NAME,
    MAKE_FUNCTION,
    CALL_FUNCTION,
    RELATIVE_JUMP,
    RELATIVE_JUMP_IF_TRUE,
)

test_bytecode = [
    [LOAD_CONST(1)],
    [LOAD_CONST(1), STORE_NAME("x")],
    [LOAD_NAME("x"), CALL_FUNCTION(0), RELATIVE_JUMP(0)],
    [RELATIVE_JUMP_IF_TRUE(8), MAKE_FUNCTION(3)],
]


@pytest.mark.parametrize("code", test_bytecode)
def test_serde(code):
    """assert that a roundtrip through serde is a noop"""
    assert deserialize_bytecode(serialize_bytecode(code)) == code


@pytest.mark.parametrize("code", test_bytecode)
def test_bytecode_file_io(code, tmp_path):
    """assert that a roundtrip through save/load is a noop"""
    path = tmp_path / "code.txt"
    save_bytecode(code, path)
    assert load_bytecode(path) == code


@pytest.mark.parametrize(("file", "expected"), [("factorial.lisp", "120\n")])
def test_code_file(file, expected):
    """assert strings tokenize correctly"""
    capture = io.StringIO()
    with redirect_stdout(capture):
        execute_file("test/resources/lispy/{}".format(file))
    output = capture.getvalue()
    assert output == expected
