"""bytecode instructions"""

from typing import TYPE_CHECKING

from ._opcode import Opcode

if TYPE_CHECKING:
    from typing import Any

class Instruction():
    """A compiled bytecode instruction."""

    def __init__(self, opcode, arg=None):
        # type: (Opcode, Any) -> None
        self._opcode = opcode
        self._arg = arg

    def __repr__(self):
        return "<Instruction.{}({})>".format(self._opcode, self._arg)

    def __call__(self, arg):
        return Instruction(self.opcode, arg)

    def __eq__(self, other):
        return isinstance(other, Instruction) and \
            self.opcode == other.opcode and \
            self.arg == other.arg

    @property
    def opcode(self):
        # type: () -> Opcode
        """The `Opcode` for this instruction."""
        return self._opcode

    @property
    def arg(self):
        # type: () -> Any
        """The configuration for this instruction instance."""
        return self._arg


LOAD_CONST = Instruction(Opcode.LOAD_CONST, 'const')
LOAD_NAME = Instruction(Opcode.LOAD_NAME, 'name')
STORE_NAME = Instruction(Opcode.STORE_NAME, 'name')
CALL_FUNCTION = Instruction(Opcode.CALL_FUNCTION, 'nargs')
RELATIVE_JUMP_IF_TRUE = Instruction(Opcode.RELATIVE_JUMP_IF_TRUE, 'off')
RELATIVE_JUMP = Instruction(Opcode.RELATIVE_JUMP, 'off')
MAKE_FUNCTION = Instruction(Opcode.MAKE_FUNCTION, 'nparam')
