"""This file contains constants used by pymemuc."""
from os import environ

# check for debug mode
DEBUG = environ.get("PYTHON_ENV") == "development"


# check for windows registry support
try:
    # flake8: noqa
    # pylint: disable=unused-import
    import winreg  # noqa

    WINREG_EN = True
except ImportError:
    if DEBUG:
        print(
            "Windows Registry is not supported on this platform, you must specify the path to memuc.exe manually"
        )
    WINREG_EN = False
