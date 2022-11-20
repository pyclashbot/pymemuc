"""This file contains constants used by pymemuc."""
from os import name

# check if running on windows
WIN32 = name == "nt"

# check for windows registry support
if WIN32:
    try:
        # flake8: noqa
        # pylint: disable=unused-import
        import winreg  # noqa

        WINREG_EN = True
    except ImportError:
        WINREG_EN = False
else:
    WINREG_EN = False

# number of times to retry a command decorated with _decorator._retryable
RETRIES = 3
