"""saving and loading from files"""

from ..core import tokenize, parse, compile_bytecode, evaluate


def execute_file(path):
    # type: (str) -> str
    """load and deserialize bytecode instructions from the file at `path`."""
    with open(path, "r") as file:
        result = evaluate(compile_bytecode(parse(tokenize(file.read()))))
        if result is not None:
            print(result)
