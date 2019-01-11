"""opcode definition"""

import enum

class AutoNumber(enum.Enum):
    """Enumeration with automatic value numbering."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        # pylint: disable=unused-argument
        return count


@enum.unique
class Opcode(AutoNumber):
    """Enumeration of Opcodes to be used in Instructions."""
    LOAD_CONST = enum.auto()
    STORE_NAME = enum.auto()
    LOAD_NAME = enum.auto()
    CALL_FUNCTION = enum.auto()
    RELATIVE_JUMP_IF_TRUE = enum.auto()
    RELATIVE_JUMP = enum.auto()
    MAKE_FUNCTION = enum.auto()
