"""This module contains decorators for functions in pymemuc."""

from functools import wraps
from typing import TYPE_CHECKING, Callable, TypeVar

try:
    from typing import Concatenate, ParamSpec
except ImportError:
    from typing_extensions import Concatenate, ParamSpec

from ._constants import RETRIES
from .exceptions import PyMemucError, PyMemucTimeoutExpired

if TYPE_CHECKING:
    from pymemuc import PyMemuc

_P = ParamSpec("_P")
_R = TypeVar("_R")


def retryable(
    func: Callable[Concatenate["PyMemuc", _P], _R]
) -> Callable[Concatenate["PyMemuc", _P], _R]:
    """Decorator to retry a function if it raises an exception.
    The number of retries is defined in pymemuc._constants.RETRIES
    After the last retry, the exception is raised.
    """

    @wraps(func)
    def wrapper(self: "PyMemuc", *args: _P.args, **kwargs: _P.kwargs) -> _R:
        fin_err = None  # track the last error
        for i in range(RETRIES):
            try:
                return func(self, *args, **kwargs)
            except (PyMemucError, PyMemucTimeoutExpired) as err:
                fin_err = err  # update the last error
                self.logger.debug(f"pymemuc._decorators._retryable: {err}")
                r_left = RETRIES - i - 1
                if r_left > 0:
                    self.logger.debug(
                        f"\tretrying {r_left} more time{'s' if r_left > 1 else ''}..."
                    )
        raise PyMemucError(f"Max retries ({RETRIES}) exceeded") from fin_err

    return wrapper
