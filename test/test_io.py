"""tests for io"""

import pytest

from lispy.io import deserialize, serialize, save, load
from lispy._instruction import LOAD_CONST, STORE_NAME, LOAD_NAME, \
    MAKE_FUNCTION, CALL_FUNCTION, RELATIVE_JUMP, RELATIVE_JUMP_IF_TRUE

test_bytecode = [
    [LOAD_CONST(1)],
    [LOAD_CONST(1), STORE_NAME('x')],
    [LOAD_NAME('x'), CALL_FUNCTION(0), RELATIVE_JUMP(0)],
    [RELATIVE_JUMP_IF_TRUE(8), MAKE_FUNCTION(3)]
]

@pytest.mark.parametrize('code', test_bytecode)
def test_serde(code):
    """assert that a roundtrip through serde is a noop"""
    assert deserialize(serialize(code)) == code

@pytest.mark.parametrize('code', test_bytecode)
def test_file_io(code, tmp_path):
    """assert that a roundtrip through save/load is a noop"""
    path = tmp_path / "code.txt"
    save(code, path)
    assert load(path) == code
