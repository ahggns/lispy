"""environment storage and closure support"""

from functools import reduce
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict

class Env():
    """A bound environment with an optional parent reference
    for closure evaluation."""

    def __init__(self, table=None, parent=None):
        # type: (Dict[str, Any], Env) -> None
        self._table = table or {}
        self._parent = parent

    def define(self, name, value):
        # type: (str, Any) -> None
        """Bind `value` to `name` in this `Env`."""
        self._table[name] = value

    def assign(self, name, value):
        # type: (str, Any) -> None
        """Bind `value` to `name` in this `Env`."""
        self.resolve(name).define(name, value)

    def lookup(self, name):
        # type: (str) -> Any
        """Return the value bound to `name` in this environment,
        or the nearest `parent` environment where `name` is bound.

        Raises `ReferenceError` if `name` is not bound in this or
        any parent `Env`.
        """
        value = self.resolve(name)._table[name]
        return value

    def resolve(self, name):
        # type: (str) -> Env
        """Return the environment where `name` is bound; this environment
         or the nearest `parent` environment where `name` is bound.

        Raises `ReferenceError` if `name` is not bound in this or
        any parent `Env`.
        """
        if name in self._table:
            return self

        if self._parent is None:
            raise ReferenceError(name)

        return self._parent.resolve(name)

    def is_defined(self, name):
        # type: (str) -> bool
        """Return whether `name` is bound in this or any parent `Env`."""
        try:
            self.resolve(name)
            return True
        except ReferenceError:
            return False


class Builtins(Env):
    """Environment containing only interpreter builtins."""

    def __init__(self):
        super(Builtins, self).__init__({
            'true': True,
            'false': False,
            '+': lambda *args: sum(args),
            '*': lambda *args: reduce(lambda a, b: a * b, args),
            '-': lambda *args: args[0] - args[1],
            '/': lambda *args: args[0] / args[1],
            'eq': lambda *args: args[0] == args[1],
            'cons': lambda *args: list(args),
            'map': lambda f, *args: [f(*e) for e in zip(*args)]
        })
