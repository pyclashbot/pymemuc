"""PyMemuc exceptions module."""

from subprocess import TimeoutExpired
from typing import Any


class PyMemucError(Exception):
    """PyMemuc error class."""

    def __init__(self, value: Any) -> None:  # noqa: ANN401, D107
        self.value = value

    def __str__(self) -> str:  # noqa: D105
        return repr(self.value)


class PyMemucException(Exception):  # noqa: N818
    """PyMemuc exception class."""

    def __init__(self, value: Any) -> None:  # noqa: ANN401, D107
        self.value = value

    def __str__(self) -> str:  # noqa: D105
        return repr(self.value)


class PyMemucIndexError(PyMemucException):
    """PyMemuc index error class."""

    def __init__(self, value: Any) -> None:  # noqa: ANN401, D107
        self.value = value

    def __str__(self) -> str:  # noqa: D105
        return repr(self.value)


class PyMemucTimeoutExpired(TimeoutExpired):
    """PyMemuc timeout error class."""

    def __init__(self, value: Any) -> None:  # noqa: ANN401, D107
        self.value = value

    def __str__(self) -> str:  # noqa: D105
        return repr(self.value)
