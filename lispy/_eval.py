"""bytecode evaluator for lisp"""

from ._env import Builtins
from ._function import Function
from ._opcode import Opcode

def evaluate(code, env=None):
    # type (List[Instruction], Env) -> Optional[Any]
    """Evaluate bytecode and return value from top of stack if present."""
    env = env or Builtins()
    program_counter = 0
    stack = []
    while program_counter < len(code):
        ins = code[program_counter]
        opcode = ins.opcode
        program_counter += 1
        if opcode == Opcode.LOAD_CONST:
            stack.append(ins.arg)
        elif opcode == Opcode.STORE_NAME:
            env.define(ins.arg, stack.pop(-1))
        elif opcode == Opcode.LOAD_NAME:
            stack.append(env.lookup(ins.arg))
        elif opcode == Opcode.CALL_FUNCTION:
            nargs = ins.arg
            args = [stack.pop(-1) for _ in range(nargs)][::-1]
            func = stack.pop(-1)
            assert callable(func)
            stack.append(func(*args))
        elif opcode == Opcode.RELATIVE_JUMP:
            off = ins.arg
            program_counter += off
        elif opcode == Opcode.RELATIVE_JUMP_IF_TRUE:
            off = ins.arg
            if stack.pop(-1):
                program_counter += off
        elif opcode == Opcode.MAKE_FUNCTION:
            nargs = ins.arg
            body = stack.pop(-1)
            params = stack.pop(-1)
            assert len(params) == nargs
            stack.append(Function(params, body, env))
        else:
            raise NotImplementedError(opcode)
    if stack:
        return stack[-1]
