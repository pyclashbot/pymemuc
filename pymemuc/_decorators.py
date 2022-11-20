"""This module contains decorators for functions in pymemuc."""

from functools import wraps

from ._constants import RETRIES
from .exceptions import PyMemucError, PyMemucTimeoutExpired


def _retryable(func):
    """Decorator to retry a function if it raises an exception.
    The number of retries is defined in pymemuc._constants.RETRIES
    After the last retry, the exception is raised.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        fin_err = None  # track the last error
        for i in range(RETRIES):
            try:
                return func(self, *args, **kwargs)
            except (PyMemucError, PyMemucTimeoutExpired) as err:
                fin_err = err  # update the last error
                if self.debug:
                    print(f"pymemuc._decorators._retryable: {err}")
                    r_left = RETRIES - i - 1
                    if r_left > 0:
                        print(
                            f"\tretrying {r_left} more time{'s' if r_left > 1 else ''}..."
                        )
        raise PyMemucError(f"Max retries ({RETRIES}) exceeded") from fin_err

    return wrapper
