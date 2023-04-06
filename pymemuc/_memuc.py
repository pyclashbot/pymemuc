"""This module contains functions for directly interacting with memuc.exe."""
from contextlib import suppress
from os.path import join, normpath
from subprocess import PIPE, CalledProcessError, Popen, TimeoutExpired
from tempfile import TemporaryFile
from typing import TYPE_CHECKING

from ._constants import WIN32, WINREG_EN
from .exceptions import PyMemucError, PyMemucException, PyMemucTimeoutExpired

if WINREG_EN:
    from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx

if WIN32:
    from subprocess import STARTF_USESHOWWINDOW, STARTUPINFO, SW_HIDE

    ST_INFO = STARTUPINFO()
    ST_INFO.dwFlags = STARTF_USESHOWWINDOW
    ST_INFO.wShowWindow = SW_HIDE
else:
    ST_INFO = None

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


def memuc_run(
    self: "PyMemuc", args: list[str], non_blocking=False, timeout=None
) -> tuple[int, str]:
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
        args += "-t"
    if self.debug:
        print("pymemuc._memuc.memuc_run:")
        print(f"\tCommand: {' '.join(args)}")
    try:
        with TemporaryFile(mode="r+") as stdout_file:
            with Popen(
                args,
                stdin=PIPE,
                stdout=stdout_file,
                stderr=PIPE,
                shell=False,
                startupinfo=ST_INFO,
            ) as process:
                try:
                    process.communicate(timeout=timeout)
                except TimeoutExpired as err:
                    process.kill()
                    process.communicate()
                    raise PyMemucTimeoutExpired(err) from err
                stdout_file.flush()
                stdout_file.seek(0)
                result = stdout_file.read()
                if self.debug:
                    if lines := result.splitlines():
                        print(f"\tOutput: {lines.pop(0)}")
                        for line in lines:
                            print(f"\t\t{line}")
                return (0, result)
    except CalledProcessError as err:
        raise PyMemucError(err) from err


# TODO: add output parsing
def check_task_status(self: "PyMemuc", task_id: str) -> tuple[int, str]:
    """Check the status of a task

    :param task_id: Asynchronous task ID
    :type task_id: str
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    return self.memuc_run(["taskstatus", task_id])
