"""This module contains functions for managing the VMs.
Functions for creating, deleting, and listing VMs are defined here.
"""
import re
from os.path import abspath, expanduser, expandvars
from typing import TYPE_CHECKING, Literal, Union

from ._decorators import _retryable
from .exceptions import PyMemucError, PyMemucIndexError, PyMemucTimeoutExpired
from .vminfo import VMInfo

if TYPE_CHECKING:
    from pymemuc import PyMemuc


@_retryable
def create_vm(self: "PyMemuc", vm_version="96") -> int:
    """Create a new VM

    :param vm_version: Android version. Defaults to "96".
    :type vm_version: str, optional
    :raises PyMemucError: an error if the vm creation failed
    :return: the index of the new VM, -1 if an error occurred but no exception was raised
    :rtype: int
    """
    status, output = self.memuc_run(["create", vm_version])
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to create VM: {output}")
    try:
        indecies = re.search(r"index:(\w)", output)
        return -1 if indecies is None else int(indecies[1])
    except AttributeError:
        return -1


@_retryable
def delete_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Delete a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was deleted successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "remove"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "remove"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to delete VM: {output}")
    return True


def clone_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    new_name=None,
    non_blocking=False,
) -> Literal[True]:
    """Clone a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param new_name: Cloned VM name. Defaults to None.
    :type new_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was cloned successfully
    :rtype: Literal[True]
    """
    new_name_cmd = ["-r", new_name] if new_name is not None else []
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "clone", *new_name_cmd], non_blocking
        )
    elif vm_name is not None:
        status, output = self.memuc_run(
            ["-n", vm_name, "clone", *new_name_cmd], non_blocking
        )
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to clone VM: {output}")
    return True


# TODO: verify functionality
def export_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    file_name="vm.ova",
    non_blocking=False,
):
    """Export a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param file_name: File name. Defaults to "vm.ova".
    :type file_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: the return code and the output of the command
    :rtype: tuple[int, str]
    """
    file_name = abspath(expandvars(expanduser(file_name)))
    if vm_index is not None:
        return self.memuc_run(
            ["-i", str(vm_index), "export", f'"{file_name}"'], non_blocking
        )
    if vm_name is not None:
        return self.memuc_run(["-n", vm_name, "export", f'"{file_name}"'], non_blocking)
    raise PyMemucIndexError("Please specify either a vm index or a vm name")


def import_vm(self: "PyMemuc", file_name="vm.ova", non_blocking=False) -> Literal[True]:
    """Import a VM from a file

    :param file_name: File name. Defaults to "vm.ova".
    :type file_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucError: an error if the vm import failed
    :return: True if the vm was imported successfully
    :rtype: Literal[True]
    """
    status, output = self.memuc_run(["import", file_name], non_blocking)
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to import VM: {output}")
    return True


@_retryable
def rename_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    new_name=None,
) -> Literal[True]:
    """Rename a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param new_name: New VM name. Defaults to None.
    :type new_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or name is specified
    :raises PyMemucError: an error if the vm rename failed
    :return: True if the vm was renamed successfully
    :rtype: Literal[True]
    """
    try:
        if vm_index is not None and new_name is not None:
            status, output = self.memuc_run(
                ["-i", str(vm_index), "rename", new_name], timeout=10
            )
        elif vm_name is not None and new_name is not None:
            status, output = self.memuc_run(
                ["-n", vm_name, "rename", new_name], timeout=10
            )
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to rename VM: {output}")
        return True
    except PyMemucTimeoutExpired as err:
        raise PyMemucError("Failed to rename VM: Timeout expired") from err


def compress_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    non_blocking=False,
) -> Literal[True]:
    """Compress a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param non_blocking: Whether to run the command in the background. Defaults to False.
    :type non_blocking: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :raises PyMemucError: an error if the vm compress failed
    :return: True if the vm was compressed successfully
    :rtype: Literal[True]
    """

    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "compress"], non_blocking)
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "compress"], non_blocking)
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to compress VM: {output}")
    return True


def list_vm_info(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    running=False,
    disk_info=False,
) -> list[VMInfo]:
    """List VM info, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param running: Whether to list only running VMs. Defaults to False.
    :type running: bool, optional
    :param disk_info: Whether to list disk info. Defaults to False.
    :type disk_info: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: a list of VM info, each VM info is a dictionary with the following keys:
                                index: VM index
                                title: VM title
                                top_level: VM top level
                                running: whether the VM is running
                                pid: VM pid
                                disk_usage: VM disk usage
    :rtype: list[VMInfo]
    """

    if vm_index is not None:
        _, output = self.memuc_run(
            [
                "-i",
                str(vm_index),
                "listvms",
                "-r" if running else "",
                "-s" if disk_info else "",
            ]
        )
    elif vm_name is not None:
        _, output = self.memuc_run(
            [
                "-n",
                vm_name,
                "listvms",
                "-r" if running else "",
                "-s" if disk_info else "",
            ]
        )
    else:
        _, output = self.memuc_run(
            ["listvms", "-r" if running else "", "-s" if disk_info else ""]
        )

    # handle when no VMs are on the system
    # memuc.exe will output a "read failed" error
    if "read failed" in output:
        return []

    output = output.split("\n")
    parsed_output = []

    # parse the output into a list of dictionaries representing the VMs
    # output will contain a list of vm values seperated by commas
    # if disk_info is True, each vm will have 6 values, otherwise 5
    for vm_str in output:
        if vm_str:
            vm_info = vm_str.split(",")
            parsed_output.append(
                {
                    "index": int(vm_info[0]),
                    "title": vm_info[1],
                    "top_level": vm_info[2],
                    "running": vm_info[3] == "1",
                    "pid": int(vm_info[4]),
                    "disk_usage": int(vm_info[5]) if disk_info else -1,
                }
            )
    return parsed_output


def vm_is_running(self: "PyMemuc", vm_index=0) -> bool:
    """Check if a VM is running

    :param vm_index: VM index. Defaults to 0.
    :type vm_index: int, optional
    :return: True if the VM is running, False otherwise
    :rtype: bool
    """
    _, output = self.memuc_run(["-i", str(vm_index), "isrunning"])
    return "Running" in output


def get_configuration_vm(
    self: "PyMemuc",
    config_key,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> str:
    """Get a VM configuration, must specify either a vm index or a vm name

    :param config_key: Configuration key, keys are noted in `configuration keys table
        <https://pymemuc.readthedocs.io/pymemuc.html#the-vm-configuration-keys-table>`_
    :type config_key: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: The configuration value
    :rtype: str
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "getconfigex", config_key]
        )
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "getconfigex", config_key])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "Value" in output
    if not success:
        raise PyMemucError(f"Failed to get VM configuration: {output}")
    return output.split("Value: ")[1].replace("\n", "").replace("\r", "")


def set_configuration_vm(
    self: "PyMemuc",
    config_key: str,
    config_value: str,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Set a VM configuration, must specify either a vm index or a vm name

    :param config_key: Configuration key, keys are noted in `configuration keys table
        <https://pymemuc.readthedocs.io/pymemuc.html#the-vm-configuration-keys-table>`_
    :type config_key: str
    :param config_value: Configuration value
    :type config_value: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm configuration was set successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "setconfigex", config_key, config_value]
        )
    elif vm_name is not None:
        status, output = self.memuc_run(
            ["-n", vm_name, "setconfigex", config_key, config_value]
        )
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to set VM configuration: {output}")
    return True


def randomize_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Randomize a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm was randomized successfully
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "randomize"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "randomize"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to randomize VM: {output}")
    return True
