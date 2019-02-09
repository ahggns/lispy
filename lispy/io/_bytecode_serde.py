"""serialize and deserialize bytecode from a newline-delimited string of instructions"""

import re

from ..core._instruction import (
    LOAD_CONST,
    LOAD_NAME,
    STORE_NAME,
    MAKE_FUNCTION,
    RELATIVE_JUMP,
    RELATIVE_JUMP_IF_TRUE,
    CALL_FUNCTION,
)

INST_RE = re.compile("([A-Z_]+)[(]([^)]+)[)]")


def serialize_bytecode(code):
    # type: (List[Instruction]) -> str
    """serialize a list of instructions to a string"""
    return "\n".join("{}({})".format(inst.opcode.name, inst.arg) for inst in code)


def deserialize_bytecode(code):
    # type: (str) -> List[Instruction]
    """deserialize a string containing serialized bytecode into a
    list of instructions.
    """
    unparsed_instructions = code.split("\n")
    tokenized_instructions = [
        INST_RE.match(inst).group(1, 2) for inst in unparsed_instructions
    ]

    instruction_builders = {
        "LOAD_CONST": lambda x: LOAD_CONST(int(x)),
        "LOAD_NAME": lambda x: LOAD_NAME(str(x)),
        "STORE_NAME": lambda x: STORE_NAME(str(x)),
        "CALL_FUNCTION": lambda x: CALL_FUNCTION(int(x)),
        "RELATIVE_JUMP_IF_TRUE": lambda x: RELATIVE_JUMP_IF_TRUE(int(x)),
        "RELATIVE_JUMP": lambda x: RELATIVE_JUMP(int(x)),
        "MAKE_FUNCTION": lambda x: MAKE_FUNCTION(int(x)),
    }

    instructions = [
        instruction_builders.get(name)(arg) for name, arg in tokenized_instructions
    ]
    return instructions
