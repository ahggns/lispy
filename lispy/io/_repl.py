import sys

from ..core import tokenize, parse, compile_bytecode, evaluate
from ..core._env import Builtins

class Repl():
    _env = Builtins()
    _history = []

    def __init__(self):
        self._repl_builtins = {
            '\\q': lambda self: self._quit(),
            '\\tokens': lambda self: self._tokens(),
            '\\tree': lambda self: self._tree(),
            '\\bytecode': lambda self: self._bytecode(),
        }

    def _quit(self):
        quit()

    def _tokens(self):
        print(tokenize(self._history[-1]))

    def _tree(self):
        print(parse(tokenize(self._history[-1])))

    def _bytecode(self):
        for inst in compile_bytecode(parse(tokenize(self._history[-1]))):
            print(inst)

    def repl(self):
        print('> ', end='', flush=True)
        try:
            statement = sys.stdin.readline().strip()
            if statement in self._repl_builtins:
                self._repl_builtins.get(statement)(self)
            else:
                self._history.append(statement)
                result = evaluate(compile_bytecode(parse(tokenize(self._history[-1]))), self._env)
                if result is not None:
                    print(result)
        except Exception as exc:
            print(repr(exc))
        self.repl()
