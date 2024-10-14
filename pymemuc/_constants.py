"""Constants used by pymemuc."""

from os import name

# check if running on windows
WIN32 = name == "nt"

# check for windows registry support
if WIN32:
    try:
        import winreg  # noqa: F401

        winreg_en = True
    except ImportError:
        winreg_en = False
else:
    winreg_en = False

WINREG_EN = winreg_en
del winreg_en

# number of times to retry a command decorated with _decorator._retryable
RETRIES = 3
