"""This module contains functions for directly interacting with memuc.exe."""
from contextlib import suppress
from os.path import join, normpath
from subprocess import PIPE, CalledProcessError, Popen, TimeoutExpired
from typing import TYPE_CHECKING, Tuple

from ._constants import WIN32, WINREG_EN
from .exceptions import PyMemucError, PyMemucException, PyMemucTimeoutExpired

if WINREG_EN:
    # pylint: disable=import-error
    from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx

ST_INFO = None
if WIN32:
    import ctypes
    from subprocess import (
        REALTIME_PRIORITY_CLASS,
        STARTF_USESHOWWINDOW,
        STARTF_USESTDHANDLES,
        STARTUPINFO,
        SW_HIDE,
    )

    ST_INFO = STARTUPINFO()
    ST_INFO.dwFlags |= (
        STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES | REALTIME_PRIORITY_CLASS
    )
    ST_INFO.wShowWindow = SW_HIDE


if TYPE_CHECKING:
    from pymemuc import PyMemuc


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
        with suppress(FileNotFoundError):
            akey = OpenKey(ConnectRegistry(None, HKEY_LOCAL_MACHINE), key)
            return str(join(normpath(QueryValueEx(akey, "InstallLocation")[0]), "Memu"))
    raise PyMemucError("MEmuc not found, is it installed?")


@staticmethod
def _terminate_process(process: Popen):
    """Terminate a process forcefully on Windows."""
    handle = ctypes.windll.kernel32.OpenProcess(1, False, process.pid)
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.CloseHandle(handle)


def memuc_run(
    self: "PyMemuc", args: list[str], non_blocking=False, timeout=None
) -> Tuple[int, str]:
    """run a command with memuc.exe.
    Memuc can support non-blocking commands, returning a task id.
    A timeout can be specified if memuc is expected to hang,
    but this will not work with non-blocking commands.

    :param args: a list of arguments to pass to memuc.exe
    :type args: list[str]
    :param non_blocking: whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :param timeout: the timeout in seconds. Defaults to None for no timeout.
    :type timeout: int, optional
    :return: the return code and the output of the command
    :rtype: tuple[int, str]
    :raises PyMemucError: an error if the command failed
    :raises PyMemucTimeoutExpired: an error if the command timed out
    """
    # sourcery skip: extract-method
    args.insert(0, self.memuc_path)
    if timeout is not None and non_blocking:
        raise PyMemucException("Cannot use timeout and non_blocking at the same time")
    if non_blocking:
        args.append("-t")
    self.logger.debug("pymemuc._memuc.memuc_run:")
    self.logger.debug(f"\tCommand: \"{' '.join(args)}\"")
    try:
        with Popen(
            args,
            shell=False,
            bufsize=-1,
            stdout=PIPE,
            stderr=PIPE,
            startupinfo=ST_INFO,
            close_fds=True,
            universal_newlines=True,
        ) as process:
            try:
                result, _ = process.communicate(timeout=timeout)
            except TimeoutExpired as err:
                if WIN32:
                    # pylint: disable=protected-access
                    self._terminate_process(process)
                else:
                    process.kill()
                result, _ = process.communicate()
                raise PyMemucTimeoutExpired(err) from err
            if lines := result.splitlines():
                self.logger.debug(f"\tOutput: {lines.pop(0)}")
                for line in lines:
                    self.logger.debug(f"\t\t{line}")
            return (0, result)
    except CalledProcessError as err:
        raise PyMemucError(err) from err


# TODO: add output parsing
def check_task_status(self: "PyMemuc", task_id: str) -> Tuple[int, str]:
    """Check the status of a task

    :param task_id: Asynchronous task ID
    :type task_id: str
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    return self.memuc_run(["taskstatus", task_id])
