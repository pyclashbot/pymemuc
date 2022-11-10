"""This module contains functions for controlling the VMs.
Functions for starting and stopping VMs are defined here.
"""
from typing import Literal

from .exceptions import PyMemucError, PyMemucIndexError


def start_vm(self, vm_index=None, vm_name=None, non_blocking=False) -> Literal[True]:
    """Start a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was started successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "start"], non_blocking)
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "start"], non_blocking)
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to start VM: {output}")
    return True


def stop_vm(self, vm_index=None, vm_name=None, non_blocking=False) -> Literal[True]:
    """Stop a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was stopped successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "stop"], non_blocking)
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "stop"], non_blocking)
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to stop VM: {output}")
    return True


def stop_all_vm(self, non_blocking=False) -> Literal[True]:
    """Stop all VMs

    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucError: an error if the vm stop failed
    :return: True if the vm was stopped successfully
    :rtype: Literal[True]
    """
    status, output = self.memuc_run(["stopall"], non_blocking)
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to stop all VMs: {output}")
    return True


def reboot_vm(self, vm_index=None, vm_name=None, non_blocking=False) -> Literal[True]:
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
