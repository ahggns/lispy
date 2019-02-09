"""user defined function support"""

from typing import TYPE_CHECKING
from ._env import Env

if TYPE_CHECKING:
    from typing import List, Tuple
    from ._instruction import Instruction


class Function:
    """
    A compiled function. Can be called with arguments.
    Contains a reference to its outer scope.
    """

    def __init__(self, params, body, env):
        # type: (Tuple[str], List[Instruction], Env) -> None
        self._params = params
        self._body = body
        self._env = env

    def __call__(self, *args):
        from ._eval import evaluate

        bound_params = dict(zip(self._params, args))
        bound_env = Env(bound_params, parent=self._env)
        return evaluate(self._body, bound_env)

    def __repr__(self):
        return "<Function{} => Instruction[...]({})>".format(
            self._params, len(self._body)
        )
