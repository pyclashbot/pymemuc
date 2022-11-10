"""This module contains functions for directly interacting with memuc.exe."""
import contextlib
from os.path import join, normpath
from subprocess import CalledProcessError, TimeoutExpired, run

from ._constants import DEBUG, WINREG_EN
from .exceptions import PyMemucError, PyMemucTimeoutExpired

if WINREG_EN:
    from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx


@staticmethod
def _get_memu_top_level() -> str:
    """locate the path of the memu directory using windows registry keys

    :return: the path of the memu directory
    :rtype: str
    :raises PyMemucError: an error if memu is not installed
    """
    if not WINREG_EN:
        raise PyMemucError("Windows Registry is not supported on this platform")
    for key in [  # keys to search for memu
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MEmu",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MEmu",
    ]:
        with contextlib.suppress(FileNotFoundError):
            akey = OpenKey(ConnectRegistry(None, HKEY_LOCAL_MACHINE), key)
            return str(join(normpath(QueryValueEx(akey, "InstallLocation")[0]), "Memu"))
    raise PyMemucError("MEmuc not found, is it installed?")


def memuc_run(self, args: list[str], non_blocking=False) -> tuple[int, str]:
    """run a command with memuc.exe

    :param args: a list of arguments to pass to memuc.exe
    :type args: list[str]
    :param non_blocking: whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :return: the return code and the output of the command
    :rtype: tuple[int, str]
    :raises PyMemucError: an error if the command failed
    """
    args.insert(0, self.memuc_path)
    args += "-t" if non_blocking else ""
    try:
        result = run(args, capture_output=True, text=True, check=True)
        if DEBUG:
            print(f"Command: {' '.join(args)}\nOutput: {result.stdout}")  # debug
        return (0, result.stdout)
    except CalledProcessError as err:
        raise PyMemucError(err) from err


def memuc_run_with_timeout(self, args: list[str], timeout=10) -> tuple[int, str]:
    """run a command with memuc.exe with a timeout

    :param args: a list of arguments to pass to memuc.exe
    :type args: list[str]
    :param timeout: the timeout in seconds. Defaults to 10.
    :type timeout: int, optional
    :return: the return code and the output of the command
    :rtype: tuple[int, str]
    :raises PyMemucError: an error if the command failed
    :raises PyMemucTimeoutExpired: an error if the command timed out
    """
    args.insert(0, self.memuc_path)
    try:
        result = run(args, capture_output=True, text=True, timeout=timeout, check=True)
        if DEBUG:
            print(f"Command: {' '.join(args)}\nOutput: {result.stdout}")  # debug
        return (0, result.stdout)
    except CalledProcessError as err:
        raise PyMemucError(err) from err
    except TimeoutExpired as err:
        raise PyMemucTimeoutExpired(err) from err


# TODO: add output parsing
def check_task_status(self, task_id):
    """Check the status of a task

    :param task_id: Asynchronous task ID
    :type task_id: str
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    return self.memuc_run(["taskstatus"], task_id)
