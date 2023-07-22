"""This module contains functions for commanding running virtual machines with memuc.exe.
Functions for interacting with running VMs are defined here."""
from typing import TYPE_CHECKING, Literal, Tuple, Union
from urllib.parse import urlparse

from ._decorators import _retryable
from .exceptions import PyMemucError, PyMemucIndexError, PyMemucTimeoutExpired

if TYPE_CHECKING:
    from pymemuc import PyMemuc


def sort_out_all_vm(self: "PyMemuc") -> bool:
    """Sort out all VMs

    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    status, output = self.memuc_run(["sortwin"])
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to sort out all VMs: {output}")
    return True


# TODO: look into bindings with https://github.com/egirault/googleplay-api
def install_apk_vm(
    self: "PyMemuc",
    apk_path,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    create_shortcut=False,
) -> Literal[True]:
    """Install an APK on a VM, must specify either a vm index or a vm name

    :param apk_path: Path to the APK
    :type apk_path: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param create_shortcut: Whether to create a shortcut. Defaults to False.
    :type create_shortcut: bool, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm apk installation was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            [
                "installapp",
                "-i",
                str(vm_index),
                apk_path,
                "-s" if create_shortcut else "",
            ]
        )
    elif vm_name is not None:
        status, output = self.memuc_run(
            [
                "installapp",
                "-n",
                vm_name,
                apk_path,
                "-s" if create_shortcut else "",
            ]
        )
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to install APK: {output}")
    return True


def uninstall_apk_vm(
    self: "PyMemuc",
    package_name,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Uninstall an APK on a VM, must specify either a vm index or a vm name

    :param package_name: Package name of the APK
    :type package_name: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm apk uninstallation was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "uninstallapp", package_name]
        )
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "uninstallapp", package_name])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to uninstall APK: {output}")
    return True


@_retryable
def start_app_vm(
    self: "PyMemuc",
    package_name,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    timeout: Union[int, None] = None,
) -> Literal[True]:
    """Start an app on a VM, must specify either a vm index or a vm name

    :param package_name: Package name of the APK
    :type package_name: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param timeout: Timeout in seconds. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm app start was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(
            ["-i", str(vm_index), "startapp", package_name], timeout=timeout
        )
    elif vm_name is not None:
        status, output = self.memuc_run(
            ["-n", vm_name, "startapp", package_name], timeout=timeout
        )
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to start app: {output}")
    return True


def stop_app_vm(
    self: "PyMemuc",
    package_name,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Stop an app on a VM, must specify either a vm index or a vm name

    :param package_name: Package name of the APK
    :type package_name: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm app stop was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "stopapp", package_name])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "stopapp", package_name])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to stop app: {output}")
    return True


def trigger_keystroke_vm(
    self: "PyMemuc",
    key: Literal["back", "home", "menu", "volumeup", "volumedown"],
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Trigger a keystroke on a VM, must specify either a vm index or a vm name

    :param key: Key to trigger
    :type key: Literal["back", "home", "menu", "volumeup", "volumedown"]
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm keystroke trigger was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "sendkey", key])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "sendkey", key])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to trigger keystroke: {output}")
    return True


def trigger_shake_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Trigger a shake on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm shake trigger was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "shake"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "shake"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to trigger shake: {output}")
    return True


def connect_internet_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Connect the internet on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm internet connection was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "connect"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "connect"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to connect internet: {output}")
    return True


def disconnect_internet_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Disconnect the internet on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "disconnect"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "disconnect"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to disconnect internet: {output}")
    return True


def input_text_vm(
    self: "PyMemuc",
    text,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Input text on a VM, must specify either a vm index or a vm name

    :param text: Text to input
    :type text: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm text input was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "input", text])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "input", text])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to input text: {output}")
    return True


def rotate_window_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Rotate the window on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm window rotation was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "rotate"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "rotate"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to rotate window: {output}")
    return True


def execute_command_vm(
    self: "PyMemuc",
    command,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Tuple[int, str]:
    """Execute a command on a VM, must specify either a vm index or a vm name

    :param command: Command to execute
    :type command: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    if vm_index is not None:
        return self.memuc_run(["-i", str(vm_index), "execcmd", f'"{command}"'])
    if vm_name is not None:
        return self.memuc_run(["-n", vm_name, "execcmd", f'"{command}"'])
    raise PyMemucIndexError("Please specify either a vm index or a vm name")


def change_gps_vm(
    self: "PyMemuc",
    latitude: float,
    longitude: float,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Literal[True]:
    """Change the GPS location on a VM, must specify either a vm index or a vm name

    :param latitude: Latitude
    :type latitude: float
    :param longitude: Longitude
    :type longitude: float
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm GPS change was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        success, output = self.memuc_run(
            ["-i", str(vm_index), "setgps", str(latitude), str(longitude)]
        )
    elif vm_name is not None:
        success, output = self.memuc_run(
            ["-n", vm_name, "setgps", str(latitude), str(longitude)]
        )
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = success == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to change GPS location: {output}")
    return True


# TODO: fix parsing of the output
def get_public_ip_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Tuple[int, str]:
    """Get the public IP of a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    if vm_index is not None:
        return self.memuc_run(
            ["-i", str(vm_index), 'execcmd "wget -O- whatismyip.akamai.com"']
        )
    if vm_name is not None:
        return self.memuc_run(
            ["-n", vm_name, 'execcmd "wget -O- whatismyip.akamai.com"']
        )
    raise PyMemucIndexError("Please specify either a vm index or a vm name")


def zoom_in_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Zoom in on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm zoom in was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "zoomin"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "zoomin"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to zoom in: {output}")
    return True


def zoom_out_vm(
    self: "PyMemuc", vm_index: Union[int, None] = None, vm_name: Union[str, None] = None
) -> Literal[True]:
    """Zoom out on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: True if the vm zoom out was successful
    :rtype: Literal[True]
    """
    if vm_index is not None:
        status, output = self.memuc_run(["-i", str(vm_index), "zoomout"])
    elif vm_name is not None:
        status, output = self.memuc_run(["-n", vm_name, "zoomout"])
    else:
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
    success = status == 0 and output is not None and "SUCCESS" in output
    if not success:
        raise PyMemucError(f"Failed to zoom in: {output}")
    return True


def get_app_info_list_vm(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    timeout=10,
) -> list[str]:
    """Get the list of apps installed on a VM, must specify either a vm index or a vm name

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param timeout: Timeout for the command. Defaults to 10.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :raises PyMemucError: an error if the command failed
    :return: the list of packages installed on the VM
    :rtype: list[str]
    """
    try:
        if vm_index is not None:
            _, output = self.memuc_run(
                ["-i", str(vm_index), "getappinfolist"],
                timeout=timeout,
                non_blocking=False,
            )
        elif vm_name is not None:
            _, output = self.memuc_run(
                ["-n", vm_name, "getappinfolist"],
                timeout=timeout,
                non_blocking=False,
            )
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        # check if 'cmd: Can't find service: package' is in the output
        if "cmd: Can't find service: package" in output:
            raise PyMemucError(
                "Failed to get the list of apps installed on the VM, "
                "please make sure the VM is running"
            )
        output = output.split("\n")
        output = [line.replace("package:", "") for line in output if line != ""]
        return output
    except PyMemucTimeoutExpired:
        return []


# TODO: debug this, it doesn't work
def set_accelerometer_vm(
    self: "PyMemuc",
    value: tuple[float, float, float],
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Tuple[int, str]:
    """Set the accelerometer on a VM, must specify either a vm index or a vm name

    :param value: the accelerometer value to set
    :type value: tuple[float, float, float]
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """

    if vm_index is not None:
        return self.memuc_run(
            [
                "-i",
                str(vm_index),
                "accelerometer",
                str(value[0]),
                str(value[1]),
                str(value[2]),
            ]
        )
    if vm_name is not None:
        return self.memuc_run(
            [
                "-n",
                vm_name,
                "accelerometer",
                str(value[0]),
                str(value[1]),
                str(value[2]),
            ]
        )
    raise PyMemucIndexError("Please specify either a vm index or a vm name")


def create_app_shortcut_vm(
    self: "PyMemuc",
    package_name: str,
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
) -> Tuple[int, str]:
    """Create an app shortcut on a VM, must specify either a vm index or a vm name

    :param package_name: Package name
    :type package_name: str
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :raises PyMemucTimeoutExpired: an error if the command times out
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    if vm_index is not None:
        return self.memuc_run(
            ["-i", str(vm_index), "createshortcut", package_name],
            timeout=10,
            non_blocking=False,
        )  # can raise timeout
    if vm_name is not None:
        return self.memuc_run(
            ["-n", vm_name, "createshortcut", package_name],
            timeout=10,
            non_blocking=False,
        )  # can raise timeout
    raise PyMemucIndexError("Please specify either a vm index or a vm name")


# TODO: parse the output to confirm that the command was ran successfully
def send_adb_command_vm(
    self: "PyMemuc",
    command: Union[str, list[str]],
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    timeout: Union[int, None] = None,
) -> str:
    """Send an ADB command to a VM, must specify either a vm index or a vm name

    :param command: ADB command
    :type command: str | list[str]
    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param timeout: Timeout for the command. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :raises PyMemucTimeoutExpired: an error if the command times out
    :return: the return code and the output of the command.
    :rtype: tuple[int, str]
    """
    if isinstance(command, str):
        command = command.split()
    if vm_index is not None:
        _, output = self.memuc_run(
            ["-i", str(vm_index), "adb"] + command, timeout=timeout
        )
        return output
    if vm_name is not None:
        _, output = self.memuc_run(["-n", vm_name, "adb"] + command, timeout=timeout)
        return output

    raise PyMemucIndexError("Please specify either a vm index or a vm name")


def get_adb_connection(
    self: "PyMemuc",
    vm_index: Union[int, None] = None,
    vm_name: Union[str, None] = None,
    timeout: Union[int, None] = None,
) -> Tuple[Union[str, None], Union[int, None]]:
    """Get the adb connection information for a VM

    :param vm_index: VM index. Defaults to None.
    :type vm_index: int, optional
    :param vm_name: VM name. Defaults to None.
    :type vm_name: str, optional
    :param timeout: Timeout for the command. Defaults to None.
    :type timeout: int, optional
    :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
    :raises PyMemucTimeoutExpired: an error if the command times out
    :raises PyMemucError: an error if the command fails
    :return: the ip and port of the adb connection as a tuple
    :rtype: tuple[str | None, int | None]
    """
    adb_output = self.send_adb_command_vm(
        ["shell", "ifconfig"],
        vm_index=vm_index,
        vm_name=vm_name,
        timeout=timeout,
    )
    try:
        adb_output = adb_output.split("\n")[0]
        _, connection_string = adb_output.split("connected to ")
        connection_string = urlparse(f"//{connection_string}")
        return connection_string.hostname, connection_string.port
    except ValueError as err:
        raise PyMemucError(f"Failed to get adb connection: {adb_output}") from err
