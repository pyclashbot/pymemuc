"""Decorators for functions in pymemuc."""

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


def retryable(func: Callable[Concatenate["PyMemuc", _P], _R]) -> Callable[Concatenate["PyMemuc", _P], _R]:
    """Retry a function if it raises an exception.

    The number of retries is defined in pymemuc._constants.RETRIES
    After the last retry, the exception is raised.
    """

    @wraps(func)
    def wrapper(self: "PyMemuc", *args: _P.args, **kwargs: _P.kwargs) -> _R:
        fin_err = None  # track the last error
        for i in range(RETRIES):
            try:
                return func(self, *args, **kwargs)
            except (PyMemucError, PyMemucTimeoutExpired) as err:  # noqa: PERF203
                fin_err = err  # update the last error
                self.logger.debug("pymemuc._decorators._retryable: %s", err)
                r_left = RETRIES - i - 1
                if r_left > 0:
                    self.logger.debug("\tretrying %d more time%s...", r_left, "s" if r_left > 1 else "")
        msg = f"Max retries ({RETRIES}) exceeded"
        raise PyMemucError(msg) from fin_err

    return wrapper
