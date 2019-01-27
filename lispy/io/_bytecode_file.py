"""saving and loading bytecode from files"""

from ._bytecode_serde import deserialize_bytecode, serialize_bytecode

def save_bytecode(code, path):
    # type: (List[Instruction], str) -> None
    """serialize and write bytecode instructions into the file at `path`."""
    with open(path, 'w') as file:
        file.write(serialize_bytecode(code))

def load_bytecode(path):
    # type: (str) -> List[Instruction]
    """load and deserialize bytecode instructions from the file at `path`."""
    with open(path, 'r') as file:
        return deserialize_bytecode(file.read())
