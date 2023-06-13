"""This module contains functions for controlling the VMs.
Functions for starting and stopping VMs are defined here.
"""
from typing import TYPE_CHECKING, Literal, Union

from ._decorators import _retryable
from .exceptions import PyMemucError, PyMemucIndexError

if TYPE_CHECKING:
    from pymemuc import PyMemuc


# pylint: disable=too-many-arguments
@_retryable
def start_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    headless=False,
    non_blocking=False,
    timeout=None,
) -> Literal[True]:
    """Start a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param headless: Whether to start the VM in headless mode. Defaults to False.
    :type headless: bool, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :param timeout: Timeout in seconds. Cannot be used if non blocking. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was started successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        args = ["-i", str(vm_index), "start"]
    elif vm_name is not None:
        args = ["-n", vm_name, "start"]
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    if headless:
        args.append("-b")
    status, output = self.memuc_run(args, non_blocking, timeout)
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to start VM: {output}")
    return True


@_retryable
def stop_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    non_blocking=False,
    timeout=None,
) -> Literal[True]:
    """Stop a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :param timeout: Timeout in seconds. Cannot be used if non blocking. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was stopped successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "stop"], non_blocking, timeout
        )
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "stop"], non_blocking, timeout)
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to stop VM: {output}")
    return True


@_retryable
def stop_all_vm(self: "PyMemuc", non_blocking=False, timeout=None) -> Literal[True]:
    """Stop all VMs

    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :param timeout: Timeout in seconds. Cannot be used if non blocking. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucError: an error if the vm stop failed
    :return: True if the vm was stopped successfully
    :rtype: Literal[True]
    """
    status, output = self.memuc_run(["stopall"], non_blocking, timeout)
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to stop all VMs: {output}")
    return True


def reboot_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    non_blocking=False,
) -> Literal[True]:
    """Reboot a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was rebooted successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "reboot"], non_blocking)
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "reboot"], non_blocking)
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to reboot VM: {output}")
    return True
