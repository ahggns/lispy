"""bytecode compiler for lisp"""

from itertools import chain
from typing import TYPE_CHECKING

from ._instruction import (
    LOAD_CONST,
    LOAD_NAME,
    STORE_NAME,
    MAKE_FUNCTION,
    RELATIVE_JUMP,
    RELATIVE_JUMP_IF_TRUE,
    CALL_FUNCTION,
)

if TYPE_CHECKING:
    from typing import Any, List, Union
    from ._instruction import Instruction


def compile_bytecode(exp):
    # type: (Union[int, float, str, List[Any]]) -> List[Instruction]
    """Compiled a parsed and tokenized expression into bytecode instructions.
    """
    if isinstance(exp, (int, float)):
        return [LOAD_CONST(exp)]
    if isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"':
        return [LOAD_CONST(exp[1:-1])]
    if isinstance(exp, list):
        assert exp, "expression list cannot be empty"  # assert non-empty
        if exp[0] == "val":
            assert len(exp) == 3, "'val' requires exactly two arguments"
            _, name, subexp = exp
            return compile_bytecode(subexp) + [STORE_NAME(name)]
        if exp[0] == "if":
            cond, true, false = exp[1:]
            compiled_true = compile_bytecode(true)
            compiled_false = compile_bytecode(false)
            return (
                compile_bytecode(cond)
                + [RELATIVE_JUMP_IF_TRUE(len(compiled_false) + 1)]
                + compiled_false
                + [RELATIVE_JUMP(len(compiled_true))]
                + compiled_true
            )
        if exp[0] == "lambda":
            _, params, body = exp
            assert isinstance(body, list), "body of lambda expression must be a list"
            if len(body) == 1:
                body = body[0]
            nparams = len(params)
            return [
                LOAD_CONST(tuple(params)),
                LOAD_CONST(tuple(compile_bytecode(body))),
                MAKE_FUNCTION(nparams),
            ]
        if exp[0] == "define":
            name, params, body = exp[1:]
            return compile_bytecode(["lambda", params, body]) + [STORE_NAME(name)]
        if exp[0] == "begin":
            return [inst for subexp in exp[1:] for inst in compile_bytecode(subexp)]
        args = exp[1:]
        nargs = len(args)
        load_func = compile_bytecode(exp[0])
        compiled_args = list(chain.from_iterable(compile_bytecode(arg) for arg in args))
        return load_func + compiled_args + [CALL_FUNCTION(nargs)]
    if isinstance(exp, str):
        return [LOAD_NAME(exp)]
    raise NotImplementedError(exp)
