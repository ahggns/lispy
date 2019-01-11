"""saving and loading from files"""

from ._serde import deserialize, serialize

def save(code, path):
    # type: (List[Instruction], str) -> None
    """serialize and write bytecode instructions into the file at `path`."""
    with open(path, 'w') as file:
        file.write(serialize(code))

def load(path):
    # type: (str) -> List[Instruction]
    """load and deserialize bytecode instructions from the file at `path`."""
    with open(path, 'r') as file:
        return deserialize(file.read())
