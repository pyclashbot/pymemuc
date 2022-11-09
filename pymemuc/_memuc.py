"""This module contains functions for directly interacting with memuc.exe."""
import contextlib
from os.path import join, normpath
from subprocess import PIPE, CalledProcessError, Popen, TimeoutExpired, check_output

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


def run(self, args: list[str], non_blocking=False) -> tuple[int, str]:
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
    with Popen(args, stdout=PIPE, shell=False) as proc:
        (out, err) = proc.communicate()
        out = out.decode("utf-8")  # convert bytes to string
        status = proc.wait()
        if err:
            raise PyMemucError(err)
        if DEBUG:
            # print the command that was run and the output for debugging
            print(f"Command: {' '.join(args)}\nOutput [{status}]: {out}")  # debug
        return status, out


def run_with_timeout(self, args: list[str], timeout=10) -> tuple[int, str]:
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
        return (1, check_output(args, timeout=timeout).decode("utf-8"))
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
    return self.run(["taskstatus"], task_id)
