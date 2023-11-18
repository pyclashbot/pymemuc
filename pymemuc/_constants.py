"""This file contains constants used by pymemuc."""
from os import name

# check if running on windows
WIN32 = name == "nt"

# check for windows registry support
if WIN32:
    try:
        # pylint: disable=unused-import
        import winreg  # pyright: ignore [reportUnusedImport]

        winreg_en = True  # pylint: disable=invalid-name
    except ImportError:
        winreg_en = False  # pylint: disable=invalid-name
else:
    winreg_en = False  # pylint: disable=invalid-name

WINREG_EN = winreg_en
del winreg_en

# number of times to retry a command decorated with _decorator._retryable
RETRIES = 3
